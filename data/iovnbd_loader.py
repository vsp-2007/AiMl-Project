"""
IO-VNBD Dataset Loader & Preprocessor for AI-ML Dead Reckoning.

Dataset Reference:
"IO-VNBD: Inertial and Odometry Benchmark Dataset for Ground Vehicle Positioning"
Authors: Uche Onyekpe, Vasile Palade, Stratis Kanarachos, Alicja Szkolnik (Coventry University).
Repository: https://github.com/onyekpeu/IO-VNBD.git

Schema Overview:
1. Vehicle CAN bus / Racelogic VBOX HD2 Dataset (prefix 'V-*.csv', 10 Hz sampling):
   - GPS Latitude, Longitude (degrees), Height (km), velocity (km/h), Heading (degrees, Compass Bearing 0-360)
   - Wheel Speeds: Front Left, Front Right, Rear Left, Rear Right (rad/s)
   - Kinematics: Indicated Longitudinal Acceleration (g), Indicated Lateral Acceleration (g), Yaw Rate (deg/s)
   - Engine/Chassis: Steering Angle, Gear, Engine Speed, Brake Pressure, Handbrake, etc.
2. Smartphone Sensor Dataset (prefix 'S-*.csv', 10 Hz IMU, 1 Hz GPS):
   - Accelerometer X, Y, Z (m/s^2), Gravity X, Y, Z (m/s^2)
   - Gyroscope Yaw, Pitch, Roll (rad/s)
   - GPS Latitude, Longitude (degrees), GPS Altitude (m), GPS Speed (km/h), GPS Orientation (degrees, Compass Bearing 0-360)
"""

import os
import sys
import re
import csv
import math
import glob
from typing import Dict, List, Tuple, Optional, Union, Any
import numpy as np
import torch
from torch.utils.data import Dataset

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sensor_fusion.coordinates import CoordinateTransformer

# Standard physics & vehicle constants
STANDARD_GRAVITY_G = 9.80665              # m/s^2
FORD_FIESTA_WHEEL_RADIUS_M = 0.298        # 195/55 R15 tyre nominal rolling radius
DEFAULT_IOVNBD_FS = 10.0                  # 10 Hz sampling frequency

# Official IO-VNBD Vehicle CAN Bus Columns (Table 3 from paper)
IOVNBD_VBOX_COLUMNS = [
    "No of GPS satellites available",
    "Time since start of day",
    "Latitude",
    "Longitude",
    "velocity",
    "Heading",
    "Height",
    "Vertical velocity",
    "Sampleperiod",
    "Steering Angle",
    "Wheel Speed Front Left",
    "Wheel Speed Front Right",
    "Wheel Speed Rear Left",
    "Wheel Speed Rear Right",
    "Yaw Rate",
    "Indicated Vehicle Speed",
    "Indicated Longitudinal Acceleration",
    "Indicated Lateral Acceleration",
    "Handbrake",
    "Gear Requested",
    "Gear",
    "Engine Speed",
    "Coolant Temperature",
    "Clutch Position",
    "Brake Pressure",
    "Brake Position",
    "Battery Voltage",
    "Air Temperature",
    "Accelerator Pedal Position",
]

# Official IO-VNBD Smartphone Sensor Columns (Table 4 from paper)
IOVNBD_SMARTPHONE_COLUMNS = [
    "GPS Latitude",
    "GPS Longitude",
    "GPS Altitude",
    "GPS Speed",
    "GPS Accuracy",
    "GPS Orientation",
    "GPS Satellites In Range",
    "Time Since Start",
    "Date",
    "Accelerometer X",
    "Accelerometer Y",
    "Accelerometer Z",
    "Gravity X",
    "Gravity Y",
    "Gravity Z",
    "Gyroscope (Yaw)",
    "Gyroscope (Pitch)",
    "Gyroscope (Roll)",
    "Magnetic Field X",
    "Magnetic Field Y",
    "Magnetic Field Z",
    "Orientation (Yaw)",
    "Orientation (Roll)",
    "Orientation (Pitch)",
]


def compass_bearing_to_enu_yaw(bearing_deg: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Converts Navigational Compass Bearing (0 deg = North, 90 deg = East, 180 deg = South, 270 deg = West)
    to Mathematical ENU Yaw (0 rad = East, pi/2 rad = North, -pi/2 rad = South, +-pi rad = West).
    Formula: psi_enu = (pi / 2) - radians(bearing) normalized to [-pi, pi].
    """
    if isinstance(bearing_deg, np.ndarray):
        b_rad = np.radians(bearing_deg)
        psi = (np.pi / 2.0) - b_rad
        return (psi + np.pi) % (2.0 * np.pi) - np.pi
    else:
        b_rad = math.radians(float(bearing_deg))
        psi = (math.pi / 2.0) - b_rad
        return (psi + math.pi) % (2.0 * math.pi) - math.pi


def enu_yaw_to_compass_bearing(yaw_rad: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Converts Mathematical ENU Yaw (0 rad = East, pi/2 rad = North)
    to Navigational Compass Bearing in degrees [0, 360).
    Formula: bearing = (90 - degrees(yaw_rad)) % 360.
    """
    if isinstance(yaw_rad, np.ndarray):
        deg = np.degrees(yaw_rad)
        return (90.0 - deg) % 360.0
    else:
        deg = math.degrees(float(yaw_rad))
        return (90.0 - deg) % 360.0


def _normalize_header(name: str) -> str:
    """Normalize column header: lowercase, strip punctuation and whitespace."""
    s = re.sub(r"[^a-zA-Z0-9]", "", name).lower()
    return s


def _convert_heading_to_enu(
    heading_deg: np.ndarray,
    gt_east: Optional[np.ndarray],
    gt_north: Optional[np.ndarray],
    gt_speed: np.ndarray,
    format_pref: str = "auto"
) -> np.ndarray:
    """
    Converts vehicle heading degrees to ENU radians (East=0, North=pi/2).
    Auto-detects whether heading_deg is Compass Bearing (0=North, 90=East)
    or ENU Cartesian angle (0=East, 90=North) by verifying travel kinematics against GPS.
    """
    if format_pref == "compass":
        return compass_bearing_to_enu_yaw(heading_deg).astype(np.float32)
    elif format_pref == "enu":
        return (((np.radians(heading_deg) + np.pi) % (2.0 * np.pi) - np.pi)).astype(np.float32)

    # Auto-detect mode: check consistency with ground-truth displacement if available
    is_compass = True  # Standard for official IO-VNBD / VBOX / Android
    if gt_east is not None and gt_north is not None and len(gt_east) > 10:
        moving = gt_speed > 2.0  # Speed > 2 m/s
        if np.count_nonzero(moving) >= 5:
            de = np.diff(gt_east)
            dn = np.diff(gt_north)
            move_mask = moving[:-1] & (np.hypot(de, dn) > 0.1)
            if np.count_nonzero(move_mask) >= 5:
                psi_travel = np.arctan2(dn[move_mask], de[move_mask])

                # Hypothesis A: Compass bearing (90 - H)
                psi_comp = compass_bearing_to_enu_yaw(heading_deg[:-1][move_mask])
                err_comp = np.mean(np.abs((psi_travel - psi_comp + np.pi) % (2.0 * np.pi) - np.pi))

                # Hypothesis B: ENU angle (H)
                psi_enu_hyp = ((np.radians(heading_deg[:-1][move_mask]) + np.pi) % (2.0 * np.pi) - np.pi)
                err_enu = np.mean(np.abs((psi_travel - psi_enu_hyp + np.pi) % (2.0 * np.pi) - np.pi))

                if err_enu < err_comp:
                    is_compass = False

    if is_compass:
        return compass_bearing_to_enu_yaw(heading_deg).astype(np.float32)
    else:
        return (((np.radians(heading_deg) + np.pi) % (2.0 * np.pi) - np.pi)).astype(np.float32)


class IOVNBDLoader:
    """
    Parser and normalizer for the IO-VNBD dataset.
    Converts raw CSV logs into standardized trajectory dictionaries and sliding-window tensors.
    """

    def __init__(
        self,
        wheel_radius_m: float = FORD_FIESTA_WHEEL_RADIUS_M,
        default_fs: float = DEFAULT_IOVNBD_FS,
        remove_gravity_from_accel: bool = False,
        heading_format: str = "auto",
    ):
        self.wheel_radius_m = wheel_radius_m
        self.default_fs = default_fs
        self.remove_gravity = remove_gravity_from_accel
        self.heading_format = heading_format

    def detect_schema_type(self, headers: List[str]) -> str:
        """
        Identify whether CSV belongs to:
        - 'vehicle': Ford Fiesta CAN bus / VBOX ('V-*.csv')
        - 'smartphone': AndroSensor smartphone log ('S-*.csv')
        - 'canonical': preprocessed [ax, ay, az, gx, gy, gz, speed, yaw_rate]
        """
        norm_headers = {_normalize_header(h) for h in headers}

        if any("indicatedlongitudinalacceleration" in h or "wheelspeed" in h or "timesincestartofday" in h or "velocitykmhr" in h for h in norm_headers):
            return "vehicle"
        elif any("accelerometerx" in h or "gyroscopeyaw" in h or "timesincestart" in h or "gpslatitude" in h for h in norm_headers):
            return "smartphone"
        elif "ax" in norm_headers and "gz" in norm_headers:
            return "canonical"
        elif "accelx" in norm_headers and "gyroz" in norm_headers:
            return "canonical"
        else:
            # Fallback heuristic: check if velocity / heading exist
            if "velocity" in norm_headers and "yawrate" in norm_headers:
                return "vehicle"
            return "unknown"

    def read_csv_to_dict(self, filepath: str) -> Dict[str, np.ndarray]:
        """
        Reads CSV file without pandas dependency using standard library csv and numpy.
        Supports UTF-8 BOM, European semicolon delimiters, and comma decimal separators.
        Returns a dict mapping normalized column names to float numpy arrays.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"IO-VNBD file not found: {filepath}")

        # Open file with utf-8-sig (handles UTF-8 with or without BOM) and latin-1 fallback
        lines: List[str] = []
        try:
            with open(filepath, "r", encoding="utf-8-sig", errors="replace") as f:
                lines = f.readlines()
        except Exception:
            with open(filepath, "r", encoding="latin-1", errors="replace") as f:
                lines = f.readlines()

        if not lines:
            raise ValueError(f"File {filepath} is empty.")

        # Check if file is a Git LFS pointer stub
        first_line = lines[0].strip()
        if first_line.startswith("version https://git-lfs"):
            raise ValueError(
                f"File '{filepath}' is a Git LFS pointer stub, not actual tabular data. "
                "Please download or smudge the LFS file or use generate_sample_iovnbd_v_csv()."
            )

        header_line = ""
        header_idx = 0
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                header_line = stripped
                header_idx = idx
                break

        if not header_line:
            raise ValueError(f"File {filepath} contains no header or data.")

        # Robust delimiter detection: count semicolons vs commas vs tabs
        n_semis = header_line.count(";")
        n_commas = header_line.count(",")
        n_tabs = header_line.count("\t")
        if n_semis > n_commas and n_semis > n_tabs:
            delimiter = ";"
        elif n_tabs > n_commas and n_tabs > n_semis:
            delimiter = "\t"
        else:
            delimiter = ","

        reader = csv.reader([header_line], delimiter=delimiter)
        original_headers = [h.strip() for h in next(reader)]

        raw_columns: Dict[str, List[float]] = {}
        for h in original_headers:
            norm_h = _normalize_header(h)
            raw_columns[norm_h] = []

        csv_reader = csv.reader(lines[header_idx + 1:], delimiter=delimiter)
        for row in csv_reader:
            if not row or len(row) < len(original_headers):
                continue
            for i, val in enumerate(row[:len(original_headers)]):
                norm_h = _normalize_header(original_headers[i])
                val_str = val.strip()
                try:
                    fval = float(val_str)
                except ValueError:
                    # Support European French comma decimal format (e.g. "-0,54" or "105,2")
                    if "," in val_str:
                        try:
                            fval = float(val_str.replace(",", "."))
                        except ValueError:
                            fval = np.nan
                    else:
                        fval = np.nan
                raw_columns[norm_h].append(fval)

        # Convert lists to float numpy arrays with interpolation for NaNs
        out_dict: Dict[str, np.ndarray] = {}
        for norm_h, val_list in raw_columns.items():
            arr = np.array(val_list, dtype=np.float64)
            if np.any(np.isnan(arr)):
                nans = np.isnan(arr)
                if np.all(nans):
                    arr[:] = 0.0
                else:
                    valid_idx = np.where(~nans)[0]
                    arr[nans] = np.interp(np.where(nans)[0], valid_idx, arr[valid_idx])
            out_dict[norm_h] = arr

        out_dict["__headers__"] = original_headers  # type: ignore
        return out_dict

    def load_csv(
        self,
        filepath: str,
        outage_windows: Optional[List[Tuple[float, float]]] = None,
        target_fs: Optional[float] = None,
        heading_format: Optional[str] = None
    ) -> Dict[str, np.ndarray]:
        """
        Loads an IO-VNBD CSV file and converts it into standard vehicular trajectory dictionary.

        Args:
            filepath: Path to CSV file.
            outage_windows: Optional list of (start_sec, end_sec) GNSS outage intervals.
            target_fs: Desired sampling rate in Hz. If None, uses detected or default 10 Hz.
            heading_format: 'auto', 'compass', or 'enu'. If None, uses self.heading_format.

        Returns:
            Standard trajectory dictionary compatible with IntelligentDeadReckoningNet and IntelligentEKF.
        """
        h_format = heading_format if heading_format is not None else self.heading_format
        raw_data = self.read_csv_to_dict(filepath)
        headers: List[str] = raw_data.pop("__headers__")  # type: ignore
        schema_type = self.detect_schema_type(headers)

        if schema_type == "vehicle":
            traj = self._parse_vehicle_schema(raw_data, heading_format=h_format)
        elif schema_type == "smartphone":
            traj = self._parse_smartphone_schema(raw_data, heading_format=h_format)
        elif schema_type == "canonical":
            traj = self._parse_canonical_schema(raw_data)
        else:
            traj = self._parse_generic_schema(raw_data)

        # Handle GNSS outages
        total_steps = len(traj["time"])
        time_arr = traj["time"]
        gps_mask = traj.get("gps_mask", np.ones(total_steps, dtype=bool)).copy()

        if outage_windows is not None:
            for start, end in outage_windows:
                outage_idx = (time_arr >= start) & (time_arr <= end)
                gps_mask[outage_idx] = False
        traj["gps_mask"] = gps_mask
        traj["outage_windows"] = outage_windows if outage_windows is not None else []

        # Resample if target_fs is requested and differs from native sampling frequency
        if target_fs is not None and abs(target_fs - traj["fs"]) > 1e-2:
            traj = self._resample_trajectory(traj, target_fs)

        return traj

    def _parse_vehicle_schema(
        self,
        data: Dict[str, np.ndarray],
        heading_format: str = "auto"
    ) -> Dict[str, np.ndarray]:
        """
        Extracts signals from official Vehicle CAN / Racelogic VBOX format.
        """
        def _get_col(candidates: List[str], fallback=None):
            for k in candidates:
                if k in data:
                    return data[k]
            for cand in candidates:
                for k in data.keys():
                    if k.startswith(cand):
                        return data[k]
            return fallback

        # 1. Time vector
        t_col = _get_col(["timesincestartofday", "sampleperiod"])
        if t_col is not None and len(t_col) > 0:
            if "sampleperiod" in next(iter(data.keys())):
                dt_step = float(t_col[0]) if len(t_col) > 0 else 0.1
                t = np.arange(len(next(iter(data.values())))) * dt_step
            else:
                t = t_col - t_col[0]
        else:
            t = np.arange(len(next(iter(data.values())))) * (1.0 / self.default_fs)

        n_samples = len(t)
        dt = float(np.median(np.diff(t))) if n_samples > 1 else (1.0 / self.default_fs)
        if dt <= 0:
            dt = 1.0 / self.default_fs
        fs = 1.0 / dt

        # 2. Forward & Lateral Accelerations
        ax_col = _get_col(["indicatedlongitudinalacceleration", "ax"])
        ax = (ax_col * STANDARD_GRAVITY_G).astype(np.float32) if ax_col is not None else np.zeros(n_samples, dtype=np.float32)

        ay_col = _get_col(["indicatedlateralacceleration", "ay"])
        ay = (ay_col * STANDARD_GRAVITY_G).astype(np.float32) if ay_col is not None else np.zeros(n_samples, dtype=np.float32)

        az = np.full(n_samples, STANDARD_GRAVITY_G, dtype=np.float32)

        # 3. Angular Velocities: Yaw Rate in deg/s -> rad/s
        gz_col = _get_col(["yawrate", "gyroz", "gz"])
        gz = np.radians(gz_col).astype(np.float32) if gz_col is not None else np.zeros(n_samples, dtype=np.float32)

        gx = np.zeros(n_samples, dtype=np.float32)
        gy = np.zeros(n_samples, dtype=np.float32)

        # 4. Wheel odometry
        wheel_speed = np.zeros(n_samples, dtype=np.float32)
        ws_keys = ["wheelspeedfrontleft", "wheelspeedfrontright", "wheelspeedrearleft", "wheelspeedrearright"]
        present_ws = [_get_col([k]) for k in ws_keys if _get_col([k]) is not None]
        if present_ws:
            avg_wheel_rads = np.mean(present_ws, axis=0)
            wheel_speed = (avg_wheel_rads * self.wheel_radius_m).astype(np.float32)

        # 5. Speed (Ground truth velocity km/h -> m/s)
        spd_col = _get_col(["velocity", "indicatedvehiclespeed", "speed"])
        if spd_col is not None:
            gt_speed = (spd_col / 3.6).astype(np.float32)
        elif present_ws:
            gt_speed = wheel_speed
        else:
            gt_speed = np.zeros(n_samples, dtype=np.float32)

        gt_speed = np.clip(gt_speed, 0.0, None)

        # 6. Heading
        hdg_col = _get_col(["heading", "gpsorientation"])
        if hdg_col is not None:
            raw_heading_deg = hdg_col
            temp_yaw = compass_bearing_to_enu_yaw(raw_heading_deg).astype(np.float32)
        else:
            raw_heading_deg = None
            temp_yaw = (np.cumsum(gz * dt) + np.pi) % (2.0 * np.pi) - np.pi
            temp_yaw = temp_yaw.astype(np.float32)

        # 7. Coordinates & Positions
        lat = _get_col(["latitude", "gpslatitude", "lat"])
        lon = _get_col(["longitude", "gpslongitude", "lon"])
        alt = _get_col(["height", "gpsaltitude", "alt"], np.zeros(n_samples))
        has_coords = (lat is not None) and (lon is not None)
        sat_col = _get_col(["noofgpssatellitesavailable", "satellites"], np.full(n_samples, 8.0))

        gt_east = np.zeros(n_samples, dtype=np.float64)
        gt_north = np.zeros(n_samples, dtype=np.float64)
        valid_gps = np.zeros(n_samples, dtype=bool)

        if has_coords:
            if np.nanmean(np.abs(alt)) < 15.0:
                alt = alt * 1000.0  # km to meters

            # Valid GPS fix criteria: non-zero, finite, and >= 4 satellites (if satellites reported)
            has_sat_reporting = (sat_col is not None and np.nanmax(sat_col) >= 4.0)
            sat_mask = (sat_col >= 4.0) if has_sat_reporting else np.ones(n_samples, dtype=bool)
            valid_gps = (
                (np.abs(lat) > 0.01) &
                (np.abs(lon) > 0.01) &
                np.isfinite(lat) &
                np.isfinite(lon) &
                sat_mask
            )

        if np.any(valid_gps):
            valid_indices = np.where(valid_gps)[0]
            first_valid = valid_indices[0]
            ref_lat = float(lat[first_valid])
            ref_lon = float(lon[first_valid])
            ref_alt = float(alt[first_valid]) if np.isfinite(alt[first_valid]) else 0.0
            transformer = CoordinateTransformer(ref_lat, ref_lon, ref_alt)

            for idx in valid_indices:
                e, n, _ = transformer.geodetic_to_enu(float(lat[idx]), float(lon[idx]), float(alt[idx]))
                gt_east[idx] = e
                gt_north[idx] = n

            # Auto-detect heading format (Compass Bearing vs ENU) using valid GPS points
            if raw_heading_deg is not None:
                gt_yaw = _convert_heading_to_enu(raw_heading_deg, gt_east, gt_north, gt_speed, format_pref=heading_format)
            else:
                gt_yaw = temp_yaw

            # 1. Backwards kinematic dead reckoning before first valid GPS fix
            for idx in range(first_valid - 1, -1, -1):
                v_step = float(gt_speed[idx + 1])
                psi_step = float(gt_yaw[idx + 1])
                gt_east[idx] = gt_east[idx + 1] - v_step * math.cos(psi_step) * dt
                gt_north[idx] = gt_north[idx + 1] - v_step * math.sin(psi_step) * dt

            # 2. Forward kinematic dead reckoning across dropouts / tunnels
            for idx in range(first_valid + 1, n_samples):
                if not valid_gps[idx]:
                    v_step = float(gt_speed[idx])
                    psi_step = float(gt_yaw[idx])
                    gt_east[idx] = gt_east[idx - 1] + v_step * math.cos(psi_step) * dt
                    gt_north[idx] = gt_north[idx - 1] + v_step * math.sin(psi_step) * dt
        else:
            # No valid GPS fixes in entire dataset: synthesize smooth kinematics from (0,0)
            gt_yaw = temp_yaw
            for i in range(1, n_samples):
                v_avg = 0.5 * (gt_speed[i - 1] + gt_speed[i])
                psi_avg = 0.5 * (gt_yaw[i - 1] + gt_yaw[i])
                gt_east[i] = gt_east[i - 1] + v_avg * math.cos(psi_avg) * dt
                gt_north[i] = gt_north[i - 1] + v_avg * math.sin(psi_avg) * dt

        # 8. GPS Observations & Masks
        gps_mask = valid_gps.copy()
        gps_east = gt_east.copy()
        gps_north = gt_north.copy()
        gps_speed = gt_speed.copy().astype(np.float64)
        gps_bearing = gt_yaw.copy().astype(np.float64)

        return {
            "time": t.astype(np.float64),
            "dt": float(dt),
            "fs": float(fs),
            "accel_x": ax,
            "accel_y": ay,
            "accel_z": az,
            "gyro_x": gx,
            "gyro_y": gy,
            "gyro_z": gz,
            "gt_speed": gt_speed,
            "gt_yaw_rate": gz,
            "gt_yaw": gt_yaw,
            "gt_east": gt_east.astype(np.float32),
            "gt_north": gt_north.astype(np.float32),
            "gps_mask": gps_mask,
            "gps_east": gps_east,
            "gps_north": gps_north,
            "gps_speed": gps_speed,
            "gps_bearing": gps_bearing,
            "wheel_speed": wheel_speed,
        }

    def _parse_smartphone_schema(
        self,
        data: Dict[str, np.ndarray],
        heading_format: str = "auto"
    ) -> Dict[str, np.ndarray]:
        """
        Extracts signals from official Smartphone AndroSensor format.
        """
        def _get_col(candidates: List[str], fallback=None):
            for k in candidates:
                if k in data:
                    return data[k]
            for cand in candidates:
                for k in data.keys():
                    if k.startswith(cand):
                        return data[k]
            return fallback

        # Time vector in ms -> seconds
        t_col = _get_col(["timesincestart", "timesincestartms", "time"])
        if t_col is not None:
            t = (t_col - t_col[0]) / 1000.0 if t_col[0] > 1000.0 or t_col[-1] > 1000.0 else (t_col - t_col[0])
        else:
            t = np.arange(len(next(iter(data.values())))) * (1.0 / self.default_fs)

        n_samples = len(t)
        dt = float(np.median(np.diff(t))) if n_samples > 1 else (1.0 / self.default_fs)
        if dt <= 0:
            dt = 1.0 / self.default_fs
        fs = 1.0 / dt

        # Accelerations in m/s^2
        ax = _get_col(["accelerometerx", "accelerometerxms", "ax"], np.zeros(n_samples)).astype(np.float32)
        ay = _get_col(["accelerometery", "accelerometeryms", "ay"], np.zeros(n_samples)).astype(np.float32)
        az = _get_col(["accelerometerz", "accelerometerzms", "az"], np.full(n_samples, STANDARD_GRAVITY_G)).astype(np.float32)

        # Optionally subtract gravity if gravity vectors are present
        gx_col = _get_col(["gravityx", "gravityxms"])
        gy_col = _get_col(["gravityy", "gravityyms"])
        gz_col = _get_col(["gravityz", "gravityzms"])
        if self.remove_gravity and gx_col is not None and gy_col is not None and gz_col is not None:
            ax = ax - gx_col.astype(np.float32)
            ay = ay - gy_col.astype(np.float32)
            az = az - gz_col.astype(np.float32)

        # Gyroscopes (rad/s)
        gz = _get_col(["gyroscopeyaw", "gyroscopeyawrads", "gyroscopez", "gz"], np.zeros(n_samples)).astype(np.float32)
        gy = _get_col(["gyroscopepitch", "gyroscopepitchrads", "gyroscopey", "gy"], np.zeros(n_samples)).astype(np.float32)
        gx = _get_col(["gyroscoperoll", "gyroscoperollrads", "gyroscopex", "gx"], np.zeros(n_samples)).astype(np.float32)

        # Ground truth speed from GPS (km/h -> m/s)
        spd_col = _get_col(["gpsspeed", "gpsspeedkmh", "speed"])
        if spd_col is not None:
            gt_speed = np.clip(spd_col / 3.6, 0.0, None).astype(np.float32)
        else:
            gt_speed = np.zeros(n_samples, dtype=np.float32)

        # Heading degrees from GPS orientation or Android orientation yaw
        heading_col = _get_col(["gpsorientation", "orientationyaw", "heading"])
        if heading_col is not None:
            raw_heading_deg = heading_col
            temp_yaw = compass_bearing_to_enu_yaw(raw_heading_deg).astype(np.float32)
        else:
            raw_heading_deg = None
            temp_yaw = (np.cumsum(gz * dt) + np.pi) % (2.0 * np.pi) - np.pi
            temp_yaw = temp_yaw.astype(np.float32)

        # Coordinates
        lat = _get_col(["gpslatitude", "gpslatitudedegrees", "lat", "latitude"])
        lon = _get_col(["gpslongitude", "gpslongitudedegrees", "lon", "longitude"])
        alt = _get_col(["gpsaltitude", "gpsaltitudem", "alt", "altitude"], np.zeros(n_samples))
        has_gps = (lat is not None) and (lon is not None)
        sat_col = _get_col(["gpssatellitesinrange", "satellites"])
        has_sat_reporting = (sat_col is not None and np.nanmax(sat_col) >= 4.0)
        sat_mask = (sat_col >= 4.0) if has_sat_reporting else np.ones(n_samples, dtype=bool)

        gt_east = np.zeros(n_samples, dtype=np.float64)
        gt_north = np.zeros(n_samples, dtype=np.float64)
        valid_gps = np.zeros(n_samples, dtype=bool)

        if has_gps:
            valid_gps = (
                (np.abs(lat) > 0.01) &
                (np.abs(lon) > 0.01) &
                np.isfinite(lat) &
                np.isfinite(lon) &
                sat_mask
            )

        if np.any(valid_gps):
            valid_indices = np.where(valid_gps)[0]
            first_valid = valid_indices[0]
            ref_lat = float(lat[first_valid])
            ref_lon = float(lon[first_valid])
            ref_alt = float(alt[first_valid]) if np.isfinite(alt[first_valid]) else 0.0
            transformer = CoordinateTransformer(ref_lat, ref_lon, ref_alt)

            for idx in valid_indices:
                e, n, _ = transformer.geodetic_to_enu(float(lat[idx]), float(lon[idx]), float(alt[idx]))
                gt_east[idx] = e
                gt_north[idx] = n

            # Auto-detect heading format using valid GPS displacements
            if raw_heading_deg is not None:
                gt_yaw = _convert_heading_to_enu(raw_heading_deg, gt_east, gt_north, gt_speed, format_pref=heading_format)
            else:
                gt_yaw = temp_yaw

            # 1. Backwards kinematic dead reckoning before first valid GPS fix
            for idx in range(first_valid - 1, -1, -1):
                v_step = float(gt_speed[idx + 1])
                psi_step = float(gt_yaw[idx + 1])
                gt_east[idx] = gt_east[idx + 1] - v_step * math.cos(psi_step) * dt
                gt_north[idx] = gt_north[idx + 1] - v_step * math.sin(psi_step) * dt

            # 2. Forward kinematic dead reckoning across dropouts / tunnels
            for idx in range(first_valid + 1, n_samples):
                if not valid_gps[idx]:
                    v_step = float(gt_speed[idx])
                    psi_step = float(gt_yaw[idx])
                    gt_east[idx] = gt_east[idx - 1] + v_step * math.cos(psi_step) * dt
                    gt_north[idx] = gt_north[idx - 1] + v_step * math.sin(psi_step) * dt
        else:
            gt_yaw = temp_yaw
            for i in range(1, n_samples):
                v_avg = 0.5 * (gt_speed[i - 1] + gt_speed[i])
                psi_avg = 0.5 * (gt_yaw[i - 1] + gt_yaw[i])
                gt_east[i] = gt_east[i - 1] + v_avg * math.cos(psi_avg) * dt
                gt_north[i] = gt_north[i - 1] + v_avg * math.sin(psi_avg) * dt

        gps_mask = valid_gps.copy()
        gps_east = gt_east.copy()
        gps_north = gt_north.copy()
        gps_speed = gt_speed.copy().astype(np.float64)
        gps_bearing = gt_yaw.copy().astype(np.float64)

        return {
            "time": t.astype(np.float64),
            "dt": float(dt),
            "fs": float(fs),
            "accel_x": ax,
            "accel_y": ay,
            "accel_z": az,
            "gyro_x": gx,
            "gyro_y": gy,
            "gyro_z": gz,
            "gt_speed": gt_speed,
            "gt_yaw_rate": gz,
            "gt_yaw": gt_yaw,
            "gt_east": gt_east.astype(np.float32),
            "gt_north": gt_north.astype(np.float32),
            "gps_mask": gps_mask,
            "gps_east": gps_east,
            "gps_north": gps_north,
            "gps_speed": gps_speed,
            "gps_bearing": gps_bearing,
            "wheel_speed": np.zeros(n_samples, dtype=np.float32),
        }

    def _parse_canonical_schema(self, data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Parses preprocessed or canonical format where columns are direct IMU / Kinematic names.
        """
        n_samples = len(next(iter(data.values())))
        t = data.get("time", data.get("t", np.arange(n_samples) * (1.0 / self.default_fs)))
        dt = float(np.median(np.diff(t))) if len(t) > 1 else (1.0 / self.default_fs)
        fs = 1.0 / dt

        ax = data.get("ax", data.get("accelx", np.zeros(n_samples))).astype(np.float32)
        ay = data.get("ay", data.get("accely", np.zeros(n_samples))).astype(np.float32)
        az = data.get("az", data.get("accelz", np.full(n_samples, STANDARD_GRAVITY_G))).astype(np.float32)

        gx = data.get("gx", data.get("gyrox", np.zeros(n_samples))).astype(np.float32)
        gy = data.get("gy", data.get("gyroy", np.zeros(n_samples))).astype(np.float32)
        gz = data.get("gz", data.get("gyroz", data.get("yawrate", np.zeros(n_samples)))).astype(np.float32)

        gt_speed = data.get("speed", data.get("velocity", data.get("gtspeed", np.zeros(n_samples)))).astype(np.float32)
        gt_yaw_rate = data.get("yawrate", data.get("gtyawrate", gz)).astype(np.float32)
        gt_yaw = data.get("yaw", data.get("heading", data.get("gtyaw", np.zeros(n_samples)))).astype(np.float32)

        gt_east = data.get("east", data.get("gteast", np.zeros(n_samples))).astype(np.float32)
        gt_north = data.get("north", data.get("gtnorth", np.zeros(n_samples))).astype(np.float32)

        gps_mask = data.get("gpsmask", np.ones(n_samples, dtype=bool))
        gps_east = data.get("gpseast", gt_east.copy().astype(np.float64))
        gps_north = data.get("gpsnorth", gt_north.copy().astype(np.float64))
        gps_speed = data.get("gpsspeed", gt_speed.copy().astype(np.float64))
        gps_bearing = data.get("gpsbearing", gt_yaw.copy().astype(np.float64))

        return {
            "time": t.astype(np.float64),
            "dt": float(dt),
            "fs": float(fs),
            "accel_x": ax,
            "accel_y": ay,
            "accel_z": az,
            "gyro_x": gx,
            "gyro_y": gy,
            "gyro_z": gz,
            "gt_speed": gt_speed,
            "gt_yaw_rate": gt_yaw_rate,
            "gt_yaw": gt_yaw,
            "gt_east": gt_east,
            "gt_north": gt_north,
            "gps_mask": gps_mask,
            "gps_east": gps_east,
            "gps_north": gps_north,
            "gps_speed": gps_speed,
            "gps_bearing": gps_bearing,
            "wheel_speed": data.get("wheelspeed", np.zeros(n_samples, dtype=np.float32)),
        }

    def _parse_generic_schema(self, data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """Best-effort heuristic mapping for unrecognized CSV schemas."""
        return self._parse_canonical_schema(data)

    def _resample_trajectory(self, traj: Dict[str, np.ndarray], target_fs: float) -> Dict[str, np.ndarray]:
        """
        Resamples trajectory signals from traj['fs'] to target_fs using linear interpolation.
        Unwraps angular phase for gt_yaw and gps_bearing to prevent false 180-deg boundary flips.
        """
        orig_t = traj["time"]
        duration = orig_t[-1] - orig_t[0]
        n_new = int(round(duration * target_fs)) + 1
        new_t = np.linspace(orig_t[0], orig_t[-1], n_new)
        new_dt = 1.0 / target_fs

        resampled: Dict[str, Any] = {
            "time": new_t,
            "dt": new_dt,
            "fs": target_fs,
            "outage_windows": traj.get("outage_windows", [])
        }

        angle_keys = {"gt_yaw", "gps_bearing"}

        for key, val in traj.items():
            if key in ["time", "dt", "fs", "outage_windows"]:
                continue
            if isinstance(val, np.ndarray) and len(val) == len(orig_t):
                if val.dtype == bool:
                    interp_vals = np.interp(new_t, orig_t, val.astype(float)) >= 0.5
                    resampled[key] = interp_vals
                elif key in angle_keys:
                    # Unwrap angles before linear interpolation to avoid boundary wrap spikes
                    unwrapped = np.unwrap(val)
                    interp_ang = np.interp(new_t, orig_t, unwrapped)
                    resampled[key] = (((interp_ang + np.pi) % (2.0 * np.pi) - np.pi)).astype(val.dtype)
                else:
                    resampled[key] = np.interp(new_t, orig_t, val).astype(val.dtype)
            else:
                resampled[key] = val

        return resampled

    def load_directory(
        self,
        dirpath: str,
        max_files: Optional[int] = None,
        pattern: str = "*.csv",
        outage_windows: Optional[List[Tuple[float, float]]] = None,
        target_fs: Optional[float] = None
    ) -> List[Dict[str, np.ndarray]]:
        """
        Recursively loads all valid IO-VNBD CSV files in a directory.
        Skips Git LFS pointer stubs gracefully.
        """
        if not os.path.exists(dirpath):
            raise FileNotFoundError(f"Directory not found: {dirpath}")

        matched_files = sorted(glob.glob(os.path.join(dirpath, "**", pattern), recursive=True))
        trajectories: List[Dict[str, np.ndarray]] = []

        for fpath in matched_files:
            try:
                traj = self.load_csv(fpath, outage_windows=outage_windows, target_fs=target_fs)
                trajectories.append(traj)
                if max_files is not None and len(trajectories) >= max_files:
                    break
            except (ValueError, KeyError, FileNotFoundError):
                continue

        return trajectories

    @staticmethod
    def create_sliding_windows(
        trajectories: List[Dict[str, np.ndarray]],
        window_size: int = 50,
        step: int = 5
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Slices trajectories into IMU sliding windows of shape (N, window_size, 6)
        and matching targets (speed_ms, yaw_rate_rads).
        """
        all_windows = []
        all_speeds = []
        all_yaw_rates = []

        for traj in trajectories:
            ax = traj["accel_x"]
            ay = traj["accel_y"]
            az = traj["accel_z"]
            gx = traj["gyro_x"]
            gy = traj["gyro_y"]
            gz = traj["gyro_z"]
            gt_spd = traj["gt_speed"]
            gt_yr = traj["gt_yaw_rate"]

            imu_matrix = np.column_stack([ax, ay, az, gx, gy, gz]).astype(np.float32)
            n_samples = len(imu_matrix)

            if n_samples < window_size:
                continue

            for i in range(0, n_samples - window_size + 1, step):
                win = imu_matrix[i : i + window_size]
                target_spd = gt_spd[i + window_size - 1]
                target_yr = gt_yr[i + window_size - 1]

                all_windows.append(win)
                all_speeds.append(target_spd)
                all_yaw_rates.append(target_yr)

        if not all_windows:
            return (
                np.empty((0, window_size, 6), dtype=np.float32),
                np.empty((0,), dtype=np.float32),
                np.empty((0,), dtype=np.float32)
            )

        return (
            np.array(all_windows, dtype=np.float32),
            np.array(all_speeds, dtype=np.float32),
            np.array(all_yaw_rates, dtype=np.float32)
        )


class IOVNBDDataset(Dataset):
    """
    PyTorch Dataset wrapper for IO-VNBD sliding windows.
    Compatible with torch.utils.data.DataLoader.
    """

    def __init__(
        self,
        trajectories: Union[List[Dict[str, np.ndarray]], str],
        window_size: int = 50,
        step: int = 5
    ):
        if isinstance(trajectories, str):
            loader = IOVNBDLoader()
            if os.path.isdir(trajectories):
                traj_list = loader.load_directory(trajectories)
            else:
                traj_list = [loader.load_csv(trajectories)]
        else:
            traj_list = trajectories

        self.windows, self.speeds, self.yaw_rates = IOVNBDLoader.create_sliding_windows(
            traj_list, window_size=window_size, step=step
        )

    def __len__(self) -> int:
        return len(self.windows)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return (
            torch.from_numpy(self.windows[idx]),
            torch.tensor(self.speeds[idx], dtype=torch.float32),
            torch.tensor(self.yaw_rates[idx], dtype=torch.float32),
        )


# =====================================================================
# Synthetic Generator for Schema-Compliant IO-VNBD CSV Files
# =====================================================================

def generate_sample_iovnbd_v_csv(
    output_path: str,
    duration_sec: float = 60.0,
    fs: float = 10.0,
    ref_lat: float = 52.4081,
    ref_lon: float = -1.5106,
    accel_bias_g: float = 0.015,
    gyro_bias_degs: float = 1.2,
    seed: int = 42
) -> str:
    """
    Generates a synthetic vehicle dataset CSV adhering strictly to the official
    29-column IO-VNBD Ford Fiesta ECU / VBOX schema (Table 3 from paper).
    GPS Heading is generated as authentic Compass Bearing [0, 360) (0=North, 90=East).
    """
    rng = np.random.RandomState(seed)
    total_steps = int(duration_sec * fs)
    dt = 1.0 / fs
    time_arr = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    transformer = CoordinateTransformer(ref_lat, ref_lon, ref_alt_m=110.0)

    # Dynamic kinematics in ENU coordinate system
    speed_ms = 0.0
    yaw_rad = 0.0  # East = 0 rad, North = pi/2 rad
    east_m = 0.0
    north_m = 0.0

    rows = []
    wheel_radius = FORD_FIESTA_WHEEL_RADIUS_M

    for i, t in enumerate(time_arr):
        # Longitudinal acceleration and yaw rate profile
        if t < 10.0:
            target_accel = 1.5  # m/s^2
            yaw_rate_rads = 0.0
        elif t < 25.0:
            target_accel = 0.0
            yaw_rate_rads = 0.15 * math.sin(2.0 * math.pi * (t - 10.0) / 10.0)  # S-turn
        elif t < 40.0:
            target_accel = 0.0
            yaw_rate_rads = 0.12  # Left turn
        elif t < 50.0:
            target_accel = -1.2  # Decelerate
            yaw_rate_rads = 0.0
        else:
            target_accel = 0.0
            yaw_rate_rads = 0.0

        speed_ms = max(0.0, speed_ms + target_accel * dt)
        yaw_rad = (yaw_rad + yaw_rate_rads * dt + math.pi) % (2.0 * math.pi) - math.pi
        east_m += speed_ms * math.cos(yaw_rad) * dt
        north_m += speed_ms * math.sin(yaw_rad) * dt

        # Geodetic coordinates
        lat_deg, lon_deg, alt_m = transformer.enu_to_geodetic(east_m, north_m, up=0.0)

        # ECU / VBOX measurements
        velocity_kmh = speed_ms * 3.6
        # Authentic VBOX GPS Heading: Compass Bearing in degrees [0, 360) (0=North, 90=East)
        compass_bearing_deg = (90.0 - math.degrees(yaw_rad) + 360.0) % 360.0
        height_km = alt_m / 1000.0  # Height in km per Table 3
        # ISO 8855 yaw rate (deg/sec, positive for left turn)
        yaw_rate_degs = math.degrees(yaw_rate_rads) + gyro_bias_degs + rng.normal(0.0, 0.05)

        # Indicated longitudinal & lateral accelerations in 'g'
        accel_fwd_g = (target_accel / STANDARD_GRAVITY_G) + accel_bias_g + rng.normal(0.0, 0.01)
        centripetal_g = (speed_ms * yaw_rate_rads) / STANDARD_GRAVITY_G
        accel_lat_g = centripetal_g + rng.normal(0.0, 0.01)

        # Wheel speeds in rad/sec
        wheel_rot_speed = speed_ms / wheel_radius
        ws_fl = wheel_rot_speed + rng.normal(0.0, 0.1)
        ws_fr = wheel_rot_speed + rng.normal(0.0, 0.1)
        ws_rl = wheel_rot_speed + rng.normal(0.0, 0.1)
        ws_rr = wheel_rot_speed + rng.normal(0.0, 0.1)

        row = [
            int(8 + rng.randint(-1, 2)),             # No of GPS satellites available
            f"{t:.2f}",                              # Time since start of day
            f"{lat_deg:.7f}",                        # Latitude
            f"{lon_deg:.7f}",                        # Longitude
            f"{velocity_kmh:.2f}",                   # velocity (km/h)
            f"{compass_bearing_deg:.2f}",            # Heading (Compass Bearing deg)
            f"{height_km:.5f}",                      # Height (km)
            "0.00",                                  # Vertical velocity
            f"{dt:.2f}",                             # Sampleperiod
            f"{math.degrees(yaw_rate_rads) * 2.5:.1f}", # Steering Angle
            f"{ws_fl:.2f}",                          # Wheel Speed Front Left
            f"{ws_fr:.2f}",                          # Wheel Speed Front Right
            f"{ws_rl:.2f}",                          # Wheel Speed Rear Left
            f"{ws_rr:.2f}",                          # Wheel Speed Rear Right
            f"{yaw_rate_degs:.3f}",                  # Yaw Rate (deg/sec)
            f"{velocity_kmh:.2f}",                   # Indicated Vehicle Speed
            f"{accel_fwd_g:.4f}",                    # Indicated Longitudinal Acceleration (g)
            f"{accel_lat_g:.4f}",                    # Indicated Lateral Acceleration (g)
            0,                                       # Handbrake
            2 if speed_ms > 5 else 1,                # Gear Requested
            2 if speed_ms > 5 else 1,                # Gear
            int(800 + speed_ms * 120),               # Engine Speed (RPM)
            88.0,                                    # Coolant Temperature
            0,                                       # Clutch Position
            15.0 if target_accel < 0 else 0.0,       # Brake Pressure
            1 if target_accel < 0 else 0,            # Brake Position
            13.8,                                    # Battery Voltage
            16.5,                                    # Air Temperature
            int(min(100.0, max(0.0, target_accel * 40.0))) # Accelerator Pedal Position
        ]
        rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(IOVNBD_VBOX_COLUMNS)
        writer.writerows(rows)

    return output_path


def generate_sample_iovnbd_s_csv(
    output_path: str,
    duration_sec: float = 60.0,
    fs: float = 10.0,
    ref_lat: float = 52.4081,
    ref_lon: float = -1.5106,
    accel_bias: float = 0.12,
    gyro_bias: float = 0.025,
    seed: int = 43
) -> str:
    """
    Generates a synthetic smartphone dataset CSV adhering strictly to the official
    24-column IO-VNBD Smartphone AndroSensor schema (Table 4 from paper).
    GPS Orientation is generated as authentic Compass Bearing [0, 360) (0=North, 90=East).
    """
    rng = np.random.RandomState(seed)
    total_steps = int(duration_sec * fs)
    dt = 1.0 / fs
    time_arr = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    transformer = CoordinateTransformer(ref_lat, ref_lon, ref_alt_m=110.0)

    speed_ms = 0.0
    yaw_rad = 0.0
    east_m = 0.0
    north_m = 0.0

    rows = []

    for i, t in enumerate(time_arr):
        if t < 12.0:
            target_accel = 1.2
            yaw_rate_rads = 0.0
        elif t < 30.0:
            target_accel = 0.0
            yaw_rate_rads = 0.10 * math.sin(2.0 * math.pi * (t - 12.0) / 12.0)
        elif t < 45.0:
            target_accel = -1.0
            yaw_rate_rads = -0.08
        else:
            target_accel = 0.0
            yaw_rate_rads = 0.0

        speed_ms = max(0.0, speed_ms + target_accel * dt)
        yaw_rad = (yaw_rad + yaw_rate_rads * dt + math.pi) % (2.0 * math.pi) - math.pi
        east_m += speed_ms * math.cos(yaw_rad) * dt
        north_m += speed_ms * math.sin(yaw_rad) * dt

        lat_deg, lon_deg, alt_m = transformer.enu_to_geodetic(east_m, north_m, up=0.0)

        # Authentic Compass Bearing (0=North, 90=East)
        compass_bearing_deg = (90.0 - math.degrees(yaw_rad) + 360.0) % 360.0

        # Smartphone sensor axes: X forward, Y left, Z vertical
        ax = target_accel + accel_bias + rng.normal(0.0, 0.15)
        ay = (speed_ms * yaw_rate_rads) + rng.normal(0.0, 0.15)
        az = STANDARD_GRAVITY_G + rng.normal(0.0, 0.20)
        measured_yaw_rate = yaw_rate_rads + gyro_bias + rng.normal(0.0, 0.008)

        row = [
            f"{lat_deg:.7f}",                        # GPS Latitude
            f"{lon_deg:.7f}",                        # GPS Longitude
            f"{alt_m:.2f}",                          # GPS Altitude (m)
            f"{speed_ms * 3.6:.2f}",                 # GPS Speed (km/h)
            "3.5",                                   # GPS Accuracy (m)
            f"{compass_bearing_deg:.2f}",            # GPS Orientation (deg)
            int(7 + rng.randint(-1, 2)),             # GPS Satellites In Range
            int(t * 1000),                           # Time Since Start (ms)
            "2019-09-08 14-30-00_000",               # Date
            f"{ax:.4f}",                             # Accelerometer X (m/s^2)
            f"{ay:.4f}",                             # Accelerometer Y (m/s^2)
            f"{az:.4f}",                             # Accelerometer Z (m/s^2)
            "0.00",                                  # Gravity X
            "0.00",                                  # Gravity Y
            f"{STANDARD_GRAVITY_G:.2f}",             # Gravity Z
            f"{measured_yaw_rate:.4f}",              # Gyroscope (Yaw) (rad/s)
            f"{rng.normal(0.0, 0.01):.4f}",          # Gyroscope (Pitch) (rad/s)
            f"{rng.normal(0.0, 0.01):.4f}",          # Gyroscope (Roll) (rad/s)
            "18.2",                                  # Magnetic Field X (uT)
            "-22.4",                                 # Magnetic Field Y (uT)
            "44.1",                                  # Magnetic Field Z (uT)
            f"{compass_bearing_deg:.2f}",            # Orientation (Yaw)
            "0.00",                                  # Orientation (Roll)
            "1.20"                                   # Orientation (Pitch)
        ]
        rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(IOVNBD_SMARTPHONE_COLUMNS)
        writer.writerows(rows)

    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IO-VNBD Dataset Loader & Tool")
    parser.add_argument("--generate-samples", action="store_true", help="Generate sample IO-VNBD files in data/iovnbd_samples")
    parser.add_argument("--output-dir", type=str, default="data/iovnbd_samples", help="Output directory for sample files")
    args = parser.parse_args()

    if args.generate_samples:
        out_v = os.path.join(args.output_dir, "V-Drive_Sample1.csv")
        out_s = os.path.join(args.output_dir, "S-Drive_Sample1.csv")
        generate_sample_iovnbd_v_csv(out_v, duration_sec=120.0)
        generate_sample_iovnbd_s_csv(out_s, duration_sec=120.0)
        print(f"[IO-VNBD] Generated sample vehicle CSV: {out_v}")
        print(f"[IO-VNBD] Generated sample smartphone CSV: {out_s}")
        loader = IOVNBDLoader()
        traj_v = loader.load_csv(out_v)
        traj_s = loader.load_csv(out_s)
        print(f"[IO-VNBD] Verification: Loaded V ({len(traj_v['time'])} steps) and S ({len(traj_s['time'])} steps) successfully.")
