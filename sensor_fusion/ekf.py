import math
import numpy as np
from typing import Optional, Tuple, Dict, Any

def normalize_angle(angle: float) -> float:
    """Normalize angle to [-pi, pi] radians."""
    a = (angle + math.pi) % (2.0 * math.pi) - math.pi
    if a == -math.pi and angle > 0:
        return math.pi
    return a

class IntelligentEKF:
    """
    Intelligent Extended Kalman Filter (IEKF) for seamless Dead Reckoning
    and GNSS/IMU sensor fusion.
    
    State Vector x (5x1):
    0: p_e   - East position (meters)
    1: p_n   - North position (meters)
    2: v     - Forward velocity (m/s)
    3: psi   - Yaw / Heading angle in radians (from East towards North)
    4: b_yaw - Gyro yaw rate bias (rad/s)
    """

    def __init__(
        self,
        init_east: float = 0.0,
        init_north: float = 0.0,
        init_velocity: float = 0.0,
        init_yaw_rad: float = 0.0,
        q_pos: float = 0.05,
        q_vel: float = 0.2,
        q_yaw: float = 0.01,
        q_bias: float = 1e-4,
    ):
        # State vector
        self.x = np.array([
            init_east,
            init_north,
            init_velocity,
            normalize_angle(init_yaw_rad),
            0.0  # initial gyro yaw bias
        ], dtype=np.float64)

        # State covariance P
        self.P = np.diag([
            4.0,       # pos_e variance (m^2)
            4.0,       # pos_n variance (m^2)
            1.0,       # velocity variance ((m/s)^2)
            0.05,      # yaw variance (rad^2)
            0.001      # bias variance ((rad/s)^2)
        ]).astype(np.float64)

        # Base Process noise covariance parameters
        self.q_pos = q_pos
        self.q_vel = q_vel
        self.q_yaw = q_yaw
        self.q_bias = q_bias

        # Diagnostic counters and tracking
        self.last_timestamp: Optional[float] = None
        self.prev_psi: float = normalize_angle(init_yaw_rad)
        self.last_gyro_yaw_rate: float = 0.0
        self.outage_active: bool = False
        self.outage_duration_s: float = 0.0
        self.total_distance_m: float = 0.0

    def predict(self, dt: float, accel_fwd: float, gyro_yaw_rate: float, q_scale: float = 1.0) -> np.ndarray:
        """
        EKF Prediction step using IMU inputs.
        accel_fwd: forward acceleration (m/s^2)
        gyro_yaw_rate: yaw angular rate (rad/s)
        """
        if dt <= 0.0 or dt > 1.0:
            dt = 0.02  # default 50Hz fallback if timestamp jitter occurs

        p_e, p_n, v, psi, b_yaw = self.x
        self.prev_psi = psi
        self.last_gyro_yaw_rate = gyro_yaw_rate

        # Compensate yaw rate with estimated bias
        corrected_yaw_rate = gyro_yaw_rate - b_yaw
        half_turn = psi + 0.5 * corrected_yaw_rate * dt

        # Update position using mid-interval heading for 2nd order precision
        new_pe = p_e + v * math.cos(half_turn) * dt
        new_pn = p_n + v * math.sin(half_turn) * dt
        new_v = max(0.0, v + accel_fwd * dt)  # non-holonomic vehicle assumption (forward motion)
        new_psi = normalize_angle(psi + corrected_yaw_rate * dt)
        new_b_yaw = b_yaw

        self.x = np.array([new_pe, new_pn, new_v, new_psi, new_b_yaw], dtype=np.float64)
        
        # Accumulate odometer distance
        self.total_distance_m += v * dt

        # Jacobian F = df/dx
        F = np.eye(5, dtype=np.float64)
        F[0, 2] = math.cos(half_turn) * dt
        F[0, 3] = -v * math.sin(half_turn) * dt
        F[0, 4] = 0.5 * v * math.sin(half_turn) * (dt ** 2)

        F[1, 2] = math.sin(half_turn) * dt
        F[1, 3] = v * math.cos(half_turn) * dt
        F[1, 4] = -0.5 * v * math.cos(half_turn) * (dt ** 2)

        F[3, 4] = -dt

        # Process noise covariance Q
        # Scaled dynamically if outage is active or high dynamics detected
        scale = q_scale * (2.0 if self.outage_active else 1.0)
        Q = np.diag([
            self.q_pos * dt * scale,
            self.q_pos * dt * scale,
            self.q_vel * dt * scale,
            self.q_yaw * dt * scale,
            self.q_bias * dt
        ]).astype(np.float64)

        self.P = F @ self.P @ F.T + Q
        # Ensure symmetry
        self.P = 0.5 * (self.P + self.P.T)
        return self.x.copy()

    def update_gnss(
        self,
        east: float,
        north: float,
        speed: Optional[float] = None,
        bearing_rad: Optional[float] = None,
        pos_accuracy_m: float = 3.0,
        speed_accuracy_ms: float = 0.5,
        bearing_accuracy_rad: float = 0.15
    ) -> Dict[str, Any]:
        """
        EKF Measurement Update with GNSS data.
        Fuses 2D position (East, North), speed, and heading (if speed > 1.5 m/s).
        """
        self.outage_active = False
        self.outage_duration_s = 0.0

        measurements = [east, north]
        h_rows = [
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0, 0.0]
        ]
        r_diag = [pos_accuracy_m ** 2, pos_accuracy_m ** 2]

        if speed is not None and speed >= 0:
            measurements.append(speed)
            h_rows.append([0.0, 0.0, 1.0, 0.0, 0.0])
            r_diag.append(speed_accuracy_ms ** 2)

        # Only use GNSS bearing if vehicle is in reliable motion
        # (smartphone GNSS bearing is noisy/unreliable when stationary)
        has_bearing = bearing_rad is not None and (speed is not None and speed > 1.5)
        if has_bearing:
            measurements.append(normalize_angle(bearing_rad))
            h_rows.append([0.0, 0.0, 0.0, 1.0, 0.0])
            r_diag.append(bearing_accuracy_rad ** 2)

        z = np.array(measurements, dtype=np.float64)
        H = np.array(h_rows, dtype=np.float64)
        R = np.diag(r_diag).astype(np.float64)

        # Innovation
        z_pred = H @ self.x
        y = z - z_pred
        if has_bearing:
            # Wrap yaw innovation to [-pi, pi]
            y[-1] = normalize_angle(y[-1])

        # Innovation covariance
        S = H @ self.P @ H.T + R
        # Kalman Gain (robust against numerical ill-conditioning)
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            K = self.P @ H.T @ np.linalg.pinv(S)

        # State update
        dx = K @ y
        self.x += dx
        self.x[3] = normalize_angle(self.x[3])

        # Joseph form covariance update for numerical stability: (I - KH) P (I - KH)^T + K R K^T
        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

        return {
            "status": "gnss_updated",
            "innovations": y.tolist(),
            "east_m": float(self.x[0]),
            "north_m": float(self.x[1]),
            "velocity_ms": float(self.x[2]),
            "yaw_rad": float(self.x[3]),
            "yaw_bias_rads": float(self.x[4])
        }

    def update_ml_prediction(
        self,
        predicted_velocity: float,
        predicted_yaw_rate: float,
        var_velocity: float = 0.25,
        var_yaw_rate: float = 0.01,
        dt: float = 0.02,
        measured_gyro_yaw_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        EKF Measurement update directly using Intelligent Deep Learning model predictions.
        Crucial during GNSS outages (tunnels/canyons): binds velocity and yaw drift without double-counting.
        """
        gyro_rate = measured_gyro_yaw_rate if measured_gyro_yaw_rate is not None else self.last_gyro_yaw_rate

        # 1. Target heading step based on ML predicted rate from pre-prediction heading
        target_heading = normalize_angle(self.prev_psi + predicted_yaw_rate * dt)

        # 2. Implied gyro bias: difference between raw gyro reading and ML predicted yaw rate
        implied_bias = gyro_rate - predicted_yaw_rate

        z = np.array([
            predicted_velocity,
            target_heading,
            implied_bias
        ], dtype=np.float64)

        H = np.array([
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float64)

        R = np.diag([
            max(1e-3, var_velocity),
            max(1e-2, var_yaw_rate),
            max(1e-3, var_yaw_rate)
        ]).astype(np.float64)

        z_pred = H @ self.x
        y = z - z_pred
        y[1] = normalize_angle(y[1])

        S = H @ self.P @ H.T + R
        try:
            K = self.P @ H.T @ np.linalg.inv(S)
        except np.linalg.LinAlgError:
            K = self.P @ H.T @ np.linalg.pinv(S)

        self.x += K @ y
        self.x[3] = normalize_angle(self.x[3])

        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

        return {
            "status": "ml_updated",
            "predicted_vel": predicted_velocity,
            "predicted_yaw_rate": predicted_yaw_rate,
            "heading_rad": float(self.x[3]),
            "yaw_bias_rads": float(self.x[4])
        }

    def update_zupt(self, measured_yaw_rate: float) -> None:
        """
        Zero Velocity Update (ZUPT) and Zero Angular Rate Update (ZARU).
        Executed when vehicle stops at a signal or parking.
        Completely resets velocity to 0 and accurately snaps the gyro bias.
        """
        z = np.array([0.0, measured_yaw_rate], dtype=np.float64)
        H = np.array([
            [0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0]   # gyro bias = measured yaw rate when stationary
        ], dtype=np.float64)

        R = np.diag([0.001, 0.0001]).astype(np.float64)

        z_pred = np.array([self.x[2], self.x[4]], dtype=np.float64)
        y = z - z_pred

        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x += K @ y
        self.x[3] = normalize_angle(self.x[3])

        I = np.eye(5, dtype=np.float64)
        IKH = I - K @ H
        self.P = IKH @ self.P @ IKH.T + K @ R @ K.T
        self.P = 0.5 * (self.P + self.P.T)

    def mark_outage(self, dt: float) -> None:
        """Mark GPS signal lost and increment outage duration."""
        self.outage_active = True
        self.outage_duration_s += dt

    def get_state(self) -> Dict[str, Any]:
        """Return full estimated state with 1-sigma uncertainty bounds."""
        diag_p = np.maximum(0.0, np.diag(self.P))
        sigma = np.sqrt(diag_p)
        return {
            "east_m": float(self.x[0]),
            "north_m": float(self.x[1]),
            "velocity_ms": float(self.x[2]),
            "yaw_rad": float(self.x[3]),
            "yaw_deg": float(math.degrees(self.x[3]) % 360.0),
            "yaw_bias_rads": float(self.x[4]),
            "pos_uncertainty_m": float(math.sqrt(self.P[0, 0] + self.P[1, 1])),
            "vel_uncertainty_ms": float(sigma[2]),
            "yaw_uncertainty_deg": float(math.degrees(sigma[3])),
            "outage_active": self.outage_active,
            "outage_duration_s": float(self.outage_duration_s),
            "total_distance_m": float(self.total_distance_m)
        }
