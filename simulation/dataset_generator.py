import math
import numpy as np
from typing import Dict, List, Tuple, Any

class VehicularTrajectoryGenerator:
    """
    Generates realistic vehicular kinematics, IMU measurements with smartphone sensor noise
    (bias drift, vibration, white noise, orientation misalignment), and ground-truth GNSS.
    
    Supports simulated GNSS outages (urban canyons, tunnels, underpasses).
    """

    def __init__(self, sampling_rate_hz: float = 50.0, seed: int = 42):
        self.fs = sampling_rate_hz
        self.dt = 1.0 / sampling_rate_hz
        self.rng = np.random.RandomState(seed)

    # Exact road centerline waypoints along MG Road, Bangalore
    # From Anil Kumble Circle (12.974938, 77.609009) to Mayo Hall / Garuda Mall (12.973033, 77.617149)
    # Extracted directly from OpenStreetMap road network
    MGROAD_WAYPOINTS = [
        [77.609009, 12.974938], [77.61101, 12.974467], [77.611037, 12.974461], [77.611066, 12.974454],
        [77.611112, 12.974442], [77.611184, 12.974426], [77.611245, 12.974413], [77.611541, 12.974342],
        [77.611588, 12.974331], [77.612831, 12.974033], [77.613772, 12.973808], [77.61379, 12.973804],
        [77.613855, 12.973788], [77.613953, 12.973766], [77.613989, 12.973757], [77.614552, 12.973633],
        [77.615193, 12.973487], [77.615303, 12.973461], [77.615654, 12.973379], [77.615712, 12.973366],
        [77.615796, 12.973347], [77.616156, 12.973267], [77.616343, 12.973226], [77.616367, 12.973221],
        [77.616608, 12.973163], [77.616809, 12.973115], [77.616868, 12.973101], [77.616899, 12.973093],
        [77.616955, 12.97308], [77.617069, 12.973053], [77.617149, 12.973033]
    ]

    def generate_bangalore_mgroad_drive(
        self,
        duration_sec: float = 60.0,
        outage_windows: List[Tuple[float, float]] = None,
        accel_bias: float = 0.04,
        gyro_bias: float = 0.015,
        vibration_amp: float = 0.2,
        tilt_pitch_deg: float = 2.0
    ) -> Dict[str, np.ndarray]:
        """
        Generates realistic mobile vehicular drive SNAPPED DIRECTLY to MG Road, Bangalore.
        Eliminates random building/grass collisions by following actual asphalt road centerline!
        Simulates GNSS signal loss under the Namma Metro overhead viaduct.
        """
        if outage_windows is None:
            # Default Metro canyon outage: from 16s to 36s (20s duration)
            outage_windows = [(16.0, 36.0)]

        nodes = self.MGROAD_WAYPOINTS
        ref_lat = nodes[0][1]
        ref_lon = nodes[0][0]

        # Convert road nodes to local ENU (East-North-Up)
        lat_rad = math.radians(ref_lat)
        m_per_deg_lat = 111132.954 - 559.822 * math.cos(2.0 * lat_rad)
        m_per_deg_lon = 111412.84 * math.cos(lat_rad)

        node_e = np.array([(pt[0] - ref_lon) * m_per_deg_lon for pt in nodes])
        node_n = np.array([(pt[1] - ref_lat) * m_per_deg_lat for pt in nodes])

        seg_dists = np.hypot(np.diff(node_e), np.diff(node_n))
        cum_dist = np.insert(np.cumsum(seg_dists), 0, 0.0)
        total_road_dist = cum_dist[-1]

        total_steps = int(duration_sec * self.fs)
        time = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

        # Smooth vehicular speed profile matching Bangalore city traffic:
        # 0-5s: Accelerate from Anil Kumble signal (0 to 16.5 m/s = 60 km/h)
        # 5-46s: Cruise along MG Road past Brigade Rd & Church St
        # 46-56s: Decelerate to stop at Mayo Hall signal
        # 56-60s: Stationary at red light (ZUPT demonstration)
        t_accel = 5.0
        t_cruise = 41.0
        t_decel = 10.0
        cruise_v = total_road_dist / (0.5 * t_accel + t_cruise + 0.5 * t_decel)

        gt_speed = np.zeros(total_steps, dtype=np.float64)
        gt_accel_fwd = np.zeros(total_steps, dtype=np.float64)

        for i, ti in enumerate(time):
            if ti < t_accel:
                a = cruise_v / t_accel
                gt_accel_fwd[i] = a
                gt_speed[i] = a * ti
            elif ti < (t_accel + t_cruise):
                gt_accel_fwd[i] = 0.0
                gt_speed[i] = cruise_v
            elif ti < (t_accel + t_cruise + t_decel):
                a = -cruise_v / t_decel
                gt_accel_fwd[i] = a
                gt_speed[i] = max(0.0, cruise_v + a * (ti - (t_accel + t_cruise)))
            else:
                gt_accel_fwd[i] = 0.0
                gt_speed[i] = 0.0

        # Arc-length position along road centerline
        s_progress = np.cumsum(gt_speed * self.dt)
        s_progress = np.clip(s_progress, 0.0, total_road_dist)

        # Smooth position interpolation on road nodes
        gt_east = np.interp(s_progress, cum_dist, node_e)
        gt_north = np.interp(s_progress, cum_dist, node_n)

        # Compute heading from road tangent vector
        de = np.gradient(gt_east, self.dt)
        dn = np.gradient(gt_north, self.dt)

        gt_yaw = np.zeros(total_steps, dtype=np.float64)
        gt_yaw_rate = np.zeros(total_steps, dtype=np.float64)

        last_valid_yaw = math.atan2(dn[1], de[1]) if len(dn) > 1 else 0.0
        for i in range(total_steps):
            if gt_speed[i] > 0.2:
                last_valid_yaw = math.atan2(dn[i], de[i])
            gt_yaw[i] = last_valid_yaw

        # Yaw rate from derivative of unwrapped heading
        unwrapped_yaw = np.unwrap(gt_yaw)
        gt_yaw_rate = np.gradient(unwrapped_yaw, self.dt)
        # Suppress yaw rate when stationary
        gt_yaw_rate[gt_speed < 0.2] = 0.0

        # Centripetal acceleration
        gt_accel_lat = gt_speed * gt_yaw_rate

        # -------------------------------------------------------------
        # Generate Realistic Noisy Smartphone IMU measurements
        # -------------------------------------------------------------
        engine_vibe_x = vibration_amp * np.sin(2.0 * np.pi * 24.0 * time)
        engine_vibe_y = vibration_amp * np.cos(2.0 * np.pi * 28.0 * time)
        engine_vibe_z = 0.5 * vibration_amp * np.sin(2.0 * np.pi * 18.0 * time)

        drift_rate_gyro = self.rng.normal(0.0, 1e-4, total_steps).cumsum()
        drift_rate_accel = self.rng.normal(0.0, 1e-4, total_steps).cumsum()

        pitch_rad = math.radians(tilt_pitch_deg)
        g = 9.80665

        # Smartphone accelerometer with gravity leakage and noise
        meas_ax = (
            gt_accel_fwd * math.cos(pitch_rad)
            - g * math.sin(pitch_rad)
            + accel_bias
            + drift_rate_accel
            + engine_vibe_x
            + self.rng.normal(0.0, 0.08, total_steps)
        )
        meas_ay = (
            gt_accel_lat
            + self.rng.normal(0.0, 0.01, total_steps).cumsum() * 0.02
            + engine_vibe_y
            + self.rng.normal(0.0, 0.08, total_steps)
        )
        meas_az = (
            g * math.cos(pitch_rad)
            + gt_accel_fwd * math.sin(pitch_rad)
            + engine_vibe_z
            + self.rng.normal(0.0, 0.12, total_steps)
        )

        meas_gx = self.rng.normal(0.0, 0.005, total_steps)
        meas_gy = self.rng.normal(0.0, 0.005, total_steps)
        meas_gz = (
            gt_yaw_rate
            + gyro_bias
            + drift_rate_gyro
            + self.rng.normal(0.0, 0.008, total_steps)
        )

        # GNSS Observations & Outages
        gps_mask = np.ones(total_steps, dtype=bool)
        for s, e in outage_windows:
            gps_mask[(time >= s) & (time <= e)] = False

        gps_noise_e = self.rng.normal(0.0, 1.2, total_steps)
        gps_noise_n = self.rng.normal(0.0, 1.2, total_steps)
        gps_east = gt_east + gps_noise_e
        gps_north = gt_north + gps_noise_n
        gps_speed = np.clip(gt_speed + self.rng.normal(0.0, 0.2, total_steps), 0.0, None)
        gps_bearing = (gt_yaw + self.rng.normal(0.0, math.radians(2.0), total_steps))

        return {
            "time": time,
            "dt": self.dt,
            "fs": self.fs,
            "ref_lat": ref_lat,
            "ref_lon": ref_lon,
            "accel_x": meas_ax.astype(np.float32),
            "accel_y": meas_ay.astype(np.float32),
            "accel_z": meas_az.astype(np.float32),
            "gyro_x": meas_gx.astype(np.float32),
            "gyro_y": meas_gy.astype(np.float32),
            "gyro_z": meas_gz.astype(np.float32),
            "gt_speed": gt_speed.astype(np.float32),
            "gt_yaw_rate": gt_yaw_rate.astype(np.float32),
            "gt_yaw": gt_yaw.astype(np.float32),
            "gt_east": gt_east.astype(np.float32),
            "gt_north": gt_north.astype(np.float32),
            "gps_mask": gps_mask,
            "gps_east": gps_east.astype(np.float32),
            "gps_north": gps_north.astype(np.float32),
            "gps_speed": gps_speed.astype(np.float32),
            "gps_bearing": gps_bearing.astype(np.float32),
            "in_outage": ~gps_mask,
        }

    def generate_synthetic_drive(
        self,
        duration_sec: float = 180.0,
        outage_windows: List[Tuple[float, float]] = None,
        accel_bias: float = 0.08,
        gyro_bias: float = 0.035, # ~2 deg/sec bias drift typical of smartphone IMU
        vibration_amp: float = 0.25,
        tilt_pitch_deg: float = 4.0
    ) -> Dict[str, np.ndarray]:
        """
        Generate a multi-maneuver drive:
        - Stationary (0-10s) -> ZUPT calibration period
        - Acceleration to 50 km/h (10-25s)
        - Cruising straight (25-50s)
        - 90 degree left turn (50-60s)
        - Straight cruising (60-80s)
        - S-curve / lane changes (80-100s)
        - 90 degree right turn (100-110s)
        - Deceleration to full stop at red light (110-125s)
        - Stationary wait (125-140s)
        - Acceleration and high speed cruise (140-180s)
        """
        if outage_windows is None:
            # Default tunnel outage: from 60s to 105s (45 seconds of complete GPS loss!)
            outage_windows = [(60.0, 105.0)]

        total_steps = int(duration_sec * self.fs)
        time = np.linspace(0.0, duration_sec, total_steps, endpoint=False)

        # Ground truth kinematic arrays
        gt_speed = np.zeros(total_steps)       # m/s
        gt_yaw_rate = np.zeros(total_steps)    # rad/s
        gt_accel_fwd = np.zeros(total_steps)   # m/s^2
        gt_yaw = np.zeros(total_steps)         # rad
        gt_east = np.zeros(total_steps)        # m
        gt_north = np.zeros(total_steps)       # m

        # Current state
        current_speed = 0.0
        current_yaw = 0.0
        current_east = 0.0
        current_north = 0.0

        for i, t in enumerate(time):
            # Target speed & steering profile based on trajectory plan
            target_accel = 0.0
            target_yaw_rate = 0.0

            if 0.0 <= t < 4.0:
                # Immediate brisk acceleration from 0 to 14 m/s (~50 km/h)
                target_accel = 14.0 / 4.0
            elif 4.0 <= t < 16.0:
                # Cruising Eastbound along avenue
                target_accel = 0.0
            elif 16.0 <= t < 24.0:
                # 90 deg left turn (+pi/2 over 8s = 0.196 rad/s) onto Northbound road
                target_yaw_rate = (math.pi / 2.0) / 8.0
                target_accel = 0.0
            elif 24.0 <= t < 45.0:
                # Cruising Northbound (Tunnel entrance)
                target_accel = 0.0
            elif 45.0 <= t < 53.0:
                # 90 deg right turn (-pi/2 over 8s) Eastbound
                target_yaw_rate = -(math.pi / 2.0) / 8.0
                target_accel = 0.0
            elif 53.0 <= t < 75.0:
                # S-curve lane changes
                target_yaw_rate = 0.15 * math.sin(2.0 * math.pi * (t - 53.0) / 10.0)
                target_accel = 0.0
            elif 75.0 <= t < 88.0:
                # Decelerate to stop at intersection
                target_accel = -14.0 / 13.0
            elif 88.0 <= t < 98.0:
                # Stopped at signal (ZUPT demonstration)
                target_accel = 0.0
                target_yaw_rate = 0.0
            elif 98.0 <= t < 108.0:
                # Accelerate to 18 m/s (~65 km/h)
                target_accel = 18.0 / 10.0
            else:
                target_accel = 0.0

            # Kinematic integration
            current_speed = max(0.0, current_speed + target_accel * self.dt)
            if current_speed < 1e-4:
                target_yaw_rate = 0.0  # vehicle cannot rotate on spot

            current_yaw += target_yaw_rate * self.dt
            current_yaw = (current_yaw + math.pi) % (2.0 * math.pi) - math.pi

            current_east += current_speed * math.cos(current_yaw) * self.dt
            current_north += current_speed * math.sin(current_yaw) * self.dt

            gt_speed[i] = current_speed
            gt_accel_fwd[i] = target_accel
            gt_yaw_rate[i] = target_yaw_rate
            gt_yaw[i] = current_yaw
            gt_east[i] = current_east
            gt_north[i] = current_north

        # Centripetal acceleration: a_lat = v * yaw_rate
        gt_accel_lat = gt_speed * gt_yaw_rate

        # -------------------------------------------------------------
        # Generate Realistic Noisy Smartphone IMU measurements
        # -------------------------------------------------------------
        # 1. High-frequency vehicle engine vibration
        engine_vibe_x = vibration_amp * np.sin(2.0 * np.pi * 25.0 * time + self.rng.uniform(0, 2*np.pi))
        engine_vibe_y = vibration_amp * np.cos(2.0 * np.pi * 32.0 * time + self.rng.uniform(0, 2*np.pi))
        engine_vibe_z = 0.5 * vibration_amp * np.sin(2.0 * np.pi * 18.0 * time)

        # 2. Random walk drift for biases
        drift_rate_gyro = self.rng.normal(0.0, 1e-4, total_steps).cumsum()
        drift_rate_accel = self.rng.normal(0.0, 1e-4, total_steps).cumsum()

        # 3. Smartphone tilt pitch angle (phone mounted at angle on dashboard)
        pitch_rad = math.radians(tilt_pitch_deg)
        g = 9.80665

        # Raw measured acceleration (Forward x, Lateral y, Vertical z)
        # Pitch causes gravity leakage: g * sin(pitch) leaks into forward axis!
        meas_ax = (
            gt_accel_fwd * math.cos(pitch_rad)
            - g * math.sin(pitch_rad)
            + accel_bias
            + drift_rate_accel
            + engine_vibe_x
            + self.rng.normal(0.0, 0.12, total_steps)
        )
        meas_ay = (
            gt_accel_lat
            + self.rng.normal(0.0, 0.02, total_steps).cumsum() * 0.05
            + engine_vibe_y
            + self.rng.normal(0.0, 0.15, total_steps)
        )
        meas_az = (
            g * math.cos(pitch_rad)
            + gt_accel_fwd * math.sin(pitch_rad)
            + engine_vibe_z
            + self.rng.normal(0.0, 0.20, total_steps)
        )

        # Raw measured gyroscope (Roll gx, Pitch gy, Yaw gz)
        meas_gx = self.rng.normal(0.0, 0.01, total_steps)
        meas_gy = self.rng.normal(0.0, 0.01, total_steps)
        meas_gz = (
            gt_yaw_rate
            + gyro_bias
            + drift_rate_gyro
            + self.rng.normal(0.0, 0.008, total_steps)
        )

        # -------------------------------------------------------------
        # Generate GNSS Observations (typically 1 Hz to 5 Hz)
        # -------------------------------------------------------------
        gps_mask = np.zeros(total_steps, dtype=bool)
        gps_east = np.full(total_steps, np.nan)
        gps_north = np.full(total_steps, np.nan)
        gps_speed = np.full(total_steps, np.nan)
        gps_bearing = np.full(total_steps, np.nan)

        # 1 Hz sampling step for GPS
        gps_step = int(self.fs)  # once every 1.0 second

        in_outage_mask = np.array([any(start <= t <= end for start, end in outage_windows) for t in time], dtype=bool)

        for idx in range(0, total_steps, gps_step):
            if not in_outage_mask[idx]:
                gps_mask[idx] = True
                # GNSS multipath / white noise ~ 2.5m std
                gps_east[idx] = gt_east[idx] + self.rng.normal(0.0, 2.0)
                gps_north[idx] = gt_north[idx] + self.rng.normal(0.0, 2.0)
                gps_speed[idx] = max(0.0, gt_speed[idx] + self.rng.normal(0.0, 0.3))
                gps_bearing[idx] = (gt_yaw[idx] + self.rng.normal(0.0, 0.08) + math.pi) % (2.0 * math.pi) - math.pi

        return {
            "time": time,
            "dt": self.dt,
            "fs": self.fs,
            "in_outage": in_outage_mask,
            # IMU inputs (6-DOF)
            "accel_x": meas_ax,
            "accel_y": meas_ay,
            "accel_z": meas_az,
            "gyro_x": meas_gx,
            "gyro_y": meas_gy,
            "gyro_z": meas_gz,
            # Ground Truth Kinematics
            "gt_speed": gt_speed,
            "gt_yaw_rate": gt_yaw_rate,
            "gt_accel_fwd": gt_accel_fwd,
            "gt_yaw": gt_yaw,
            "gt_east": gt_east,
            "gt_north": gt_north,
            # GNSS Observation
            "gps_mask": gps_mask,
            "gps_east": gps_east,
            "gps_north": gps_north,
            "gps_speed": gps_speed,
            "gps_bearing": gps_bearing,
            "outage_windows": outage_windows
        }
