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
