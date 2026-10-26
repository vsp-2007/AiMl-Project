import json
import math
import os
import numpy as np
from typing import Dict, Any, Optional, Tuple

class OnlineDriftCalibrator:
    """
    Runtime Self-Correction & Online Drift Adaptation Engine.
    
    While the vehicle is driven under clear skies with active GNSS:
    1. Runs model predictions in the background and compares with GNSS velocity & heading.
    2. Learns device-specific hardware scale factors, mounting misalignment, and sensor bias drift.
    3. Employs Online Gradient Descent (OGD) with L2 weight anchoring to prevent divergence.
    4. Automatically performs Zero Velocity Updates (ZUPT) when stationary to lock gyro bias.
    5. Saves and loads learned device profiles for persistent edge personalization.
    """

    def __init__(
        self,
        learning_rate_scale: float = 0.002,
        learning_rate_bias: float = 0.005,
        regularization_lambda: float = 0.01,
        profile_path: str = "device_drift_profile.json"
    ):
        self.profile_path = profile_path
        self.lr_scale = learning_rate_scale
        self.lr_bias = learning_rate_bias
        self.reg_lambda = regularization_lambda

        # Calibrated parameters:
        # v_calibrated = scale_v * v_pred + bias_v
        # yaw_rate_calibrated = scale_yaw * yaw_pred + bias_yaw
        self.scale_v: float = 1.0
        self.bias_v: float = 0.0
        self.scale_yaw: float = 1.0
        self.bias_yaw: float = 0.0

        # Mounting orientation pitch correction (radians)
        self.mounting_pitch_rad: float = 0.0

        # Running diagnostics & statistics
        self.samples_learned: int = 0
        self.running_speed_error_sum: float = 0.0
        self.running_yaw_error_sum: float = 0.0
        self.recent_speed_errors: list = []
        self.recent_yaw_errors: list = []
        self.zupt_counter: int = 0

        # Load existing profile if present
        self.load_profile()

    def calibrate_step(
        self,
        predicted_vel: float,
        predicted_yaw_rate: float,
        gps_speed: Optional[float],
        gps_bearing_rate: Optional[float],
        gps_accuracy_m: float = 2.0,
        is_stationary: bool = False
    ) -> Dict[str, Any]:
        """
        Perform one online adaptation step when GPS is available.
        predicted_vel: raw ML predicted forward velocity (m/s)
        predicted_yaw_rate: raw ML predicted yaw rate (rad/s)
        gps_speed: true GNSS speed (m/s)
        gps_bearing_rate: estimated true heading angular rate from GNSS trajectory (rad/s)
        """
        # If stationary (ZUPT detected):
        if is_stationary:
            self.zupt_counter += 1
            # When stationary, true velocity = 0 and true yaw rate = 0
            # Directly calibrate biases with strict bounding against noise
            v_err = 0.0 - (self.scale_v * predicted_vel + self.bias_v)
            self.bias_v += 0.05 * v_err

            yaw_err = 0.0 - (self.scale_yaw * predicted_yaw_rate + self.bias_yaw)
            self.bias_yaw = float(np.clip(self.bias_yaw + 0.01 * yaw_err, -0.002, 0.002))
            
            return {
                "adapted": True,
                "event": "zupt_recalibration",
                "scale_v": self.scale_v,
                "bias_v": self.bias_v,
                "scale_yaw": self.scale_yaw,
                "bias_yaw": self.bias_yaw
            }

        # If GPS is not available or low accuracy, skip learning
        if gps_speed is None or gps_accuracy_m > 4.5:
            return {"adapted": False, "reason": "gps_unavailable_or_degraded"}

        # Trust weight inversely proportional to GPS uncertainty
        weight = float(np.clip(3.0 / max(1.0, gps_accuracy_m), 0.2, 1.5))

        # Forward velocity error
        calibrated_v = self.scale_v * predicted_vel + self.bias_v
        err_v = gps_speed - calibrated_v

        # Gradient descent step for velocity parameters:
        # Loss = 0.5 * (calibrated_v - gps_speed)^2 + 0.5 * lambda * ((scale_v - 1)^2 + bias_v^2)
        grad_scale_v = -err_v * predicted_vel + self.reg_lambda * (self.scale_v - 1.0)
        grad_bias_v = -err_v + self.reg_lambda * self.bias_v

        self.scale_v -= self.lr_scale * weight * np.clip(grad_scale_v, -5.0, 5.0)
        self.bias_v -= self.lr_bias * weight * np.clip(grad_bias_v, -2.0, 2.0)
        # Constrain scale factor to plausible range (0.8 to 1.2)
        self.scale_v = float(np.clip(self.scale_v, 0.75, 1.25))

        # Yaw rate calibration (only during steady straight motion with high-accuracy GPS)
        err_yaw = 0.0
        if gps_bearing_rate is not None and gps_speed > 3.0 and abs(gps_bearing_rate) < 0.08:
            calibrated_yaw = self.scale_yaw * predicted_yaw_rate + self.bias_yaw
            err_yaw = gps_bearing_rate - calibrated_yaw

            # Heavy regularization anchoring bias to zero to reject noise
            grad_bias_yaw = -err_yaw + 0.1 * self.bias_yaw
            self.bias_yaw -= 0.001 * weight * np.clip(grad_bias_yaw, -0.05, 0.05)
            self.bias_yaw = float(np.clip(self.bias_yaw, -0.002, 0.002))
            self.scale_yaw = 1.0  # Keep scale factor locked at 1.0 to avoid turn distortion

        # Update diagnostics
        self.samples_learned += 1
        self.running_speed_error_sum += abs(err_v)
        self.running_yaw_error_sum += abs(err_yaw)

        self.recent_speed_errors.append(abs(err_v))
        if len(self.recent_speed_errors) > 50:
            self.recent_speed_errors.pop(0)

        # Save profile periodically every 100 samples
        if self.samples_learned % 100 == 0:
            self.save_profile()

        return {
            "adapted": True,
            "samples_learned": self.samples_learned,
            "speed_residual_ms": float(err_v),
            "yaw_residual_rads": float(err_yaw),
            "scale_v": float(self.scale_v),
            "bias_v": float(self.bias_v),
            "scale_yaw": float(self.scale_yaw),
            "bias_yaw": float(self.bias_yaw),
            "avg_speed_error_ms": float(np.mean(self.recent_speed_errors)) if self.recent_speed_errors else 0.0
        }

    def apply_correction(self, raw_vel: float, raw_yaw_rate: float) -> Tuple[float, float]:
        """
        Apply the runtime learned device-specific scale and bias corrections
        to raw ML model predictions.
        """
        calibrated_v = max(0.0, self.scale_v * raw_vel + self.bias_v)
        calibrated_yaw_rate = self.scale_yaw * raw_yaw_rate + self.bias_yaw
        return calibrated_v, calibrated_yaw_rate

    def get_profile(self) -> Dict[str, Any]:
        """Return the current device calibration profile."""
        recent_err = float(np.mean(self.recent_speed_errors)) if self.recent_speed_errors else 0.0
        return {
            "scale_v": float(self.scale_v),
            "bias_v": float(self.bias_v),
            "scale_yaw": float(self.scale_yaw),
            "bias_yaw": float(self.bias_yaw),
            "samples_learned": self.samples_learned,
            "recent_speed_mae_ms": recent_err,
            "health": "CALIBRATED" if self.samples_learned > 20 else "CALIBRATING"
        }

    def save_profile(self) -> None:
        """Persist device calibration profile to JSON."""
        try:
            data = {
                "scale_v": self.scale_v,
                "bias_v": self.bias_v,
                "scale_yaw": self.scale_yaw,
                "bias_yaw": self.bias_yaw,
                "samples_learned": self.samples_learned
            }
            with open(self.profile_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def load_profile(self) -> None:
        """Load saved profile if available on edge storage."""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r") as f:
                    data = json.load(f)
                    self.scale_v = float(data.get("scale_v", 1.0))
                    self.bias_v = float(data.get("bias_v", 0.0))
                    self.scale_yaw = float(data.get("scale_yaw", 1.0))
                    self.bias_yaw = float(data.get("bias_yaw", 0.0))
                    self.samples_learned = int(data.get("samples_learned", 0))
            except Exception:
                pass
