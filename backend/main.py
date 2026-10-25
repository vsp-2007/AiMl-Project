import math
import os
import sys
import time
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from collections import deque

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure module visibility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensor_fusion.coordinates import CoordinateTransformer
from sensor_fusion.ekf import IntelligentEKF
from models.online_calibrator import OnlineDriftCalibrator
from simulation.dataset_generator import VehicularTrajectoryGenerator
from backend.schemas import IMUPacket, GNSSPacket, TelemetryFeedRequest, SimulationStartRequest, OutageToggleRequest

app = FastAPI(
    title="SIH26168 - AI-ML Intelligent Dead Reckoning System",
    description="Edge-optimized IMU drift compensation & seamless GNSS sensor fusion engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NavigationCore:
    """
    Central real-time state manager fusing IMU streaming,
    Deep Learning dead reckoning inference, online calibration, and EKF.
    """
    def __init__(self, ref_lat: float = 12.9716, ref_lon: float = 77.5946): # Bangalore / ISRO HQ
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self.transformer = CoordinateTransformer(ref_lat, ref_lon, 0.0)

        # Intelligent EKF (AI-ML Fusion)
        self.ekf = IntelligentEKF(
            init_east=0.0,
            init_north=0.0,
            init_velocity=0.0,
            init_yaw_rad=0.0
        )

        # Baseline Naive Dead Reckoning (for comparative drift benchmarking)
        self.naive_east = 0.0
        self.naive_north = 0.0
        self.naive_vel = 0.0
        self.naive_yaw = 0.0

        # Online runtime self-correction engine
        self.calibrator = OnlineDriftCalibrator(profile_path="device_drift_profile.json")

        # Sliding IMU buffer (50 samples = 1 sec at 50Hz)
        self.window_size = 50
        self.imu_buffer = deque(maxlen=self.window_size)

        # Outage simulation flag
        self.force_outage = False
        self.last_imu_timestamp: Optional[float] = None
        self.last_gnss_bearing: Optional[float] = None
        self.last_gnss_timestamp: Optional[float] = None

        # Model handles (PyTorch or ONNX Runtime)
        self.model = None
        self.onnx_session = None
        self.device = "cpu"
        self._init_model()

    def reset(self):
        """Reset internal filter states and buffers cleanly."""
        self.ekf = IntelligentEKF(
            init_east=0.0,
            init_north=0.0,
            init_velocity=0.0,
            init_yaw_rad=0.0
        )
        self.naive_east = 0.0
        self.naive_north = 0.0
        self.naive_vel = 0.0
        self.naive_yaw = 0.0
        self.imu_buffer.clear()
        self.force_outage = False
        self.last_imu_timestamp = None
        self.last_gnss_bearing = None
        self.last_gnss_timestamp = None

    def _init_model(self):
        # 1. Try PyTorch
        try:
            import torch
            from models.idr_model import IntelligentDeadReckoningNet
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "idr_model_best.pt")
            try:
                net = IntelligentDeadReckoningNet().to(self.device)
            except Exception:
                self.device = "cpu"
                net = IntelligentDeadReckoningNet().to(self.device)
            if os.path.exists(model_path):
                ckpt = torch.load(model_path, map_location=self.device)
                net.load_state_dict(ckpt["model_state_dict"])
                print(f"[Model] Successfully loaded PyTorch weights from {model_path} on {self.device}")
            net.eval()
            self.model = net
        except Exception as e:
            self.model = None

        # 2. Try ONNX Runtime (fast edge deployment)
        if self.model is None:
            try:
                import onnxruntime as ort
                onnx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "idr_model.onnx")
                if os.path.exists(onnx_path):
                    self.onnx_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
                    print(f"[Model] Successfully loaded ONNX model from {onnx_path}")
            except Exception:
                self.onnx_session = None

    def run_ml_inference(self, imu_window: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Run inference on (50, 6) IMU window.
        Returns: (pred_velocity, var_velocity, pred_yaw_rate, var_yaw_rate)
        """
        if self.model is not None:
            try:
                import torch
                with torch.no_grad():
                    inp = torch.from_numpy(imu_window).float().unsqueeze(0).to(self.device)
                    vel, vel_var, yr, yr_var = self.model(inp)
                    return float(vel.item()), float(vel_var.item()), float(yr.item()), float(yr_var.item())
            except Exception:
                pass

        if self.onnx_session is not None:
            try:
                inp = imu_window.astype(np.float32)[np.newaxis, :, :]  # (1, 50, 6)
                outputs = self.onnx_session.run(None, {"imu_window": inp})
                return float(outputs[0][0]), float(outputs[1][0]), float(outputs[2][0]), float(outputs[3][0])
            except Exception:
                pass

        # Intelligent Signal Processing / Analytical Kinematic Fallback
        # Extracts vibration-filtered acceleration and gyro rate
        accel_fwd = np.mean(imu_window[:, 0])
        gyro_yaw = np.mean(imu_window[:, 5])

        # Stationary detection (ZUPT filter)
        accel_var = np.var(imu_window[:, 0]) + np.var(imu_window[:, 1]) + np.var(imu_window[:, 2])
        gyro_var = np.var(imu_window[:, 3]) + np.var(imu_window[:, 4]) + np.var(imu_window[:, 5])

        if accel_var < 0.04 and gyro_var < 0.002:
            return 0.0, 0.01, 0.0, 0.0005

        current_v = max(0.0, self.ekf.x[2] + (accel_fwd - self.calibrator.bias_v) * 0.02)
        return current_v, 0.25, float(gyro_yaw), 0.005

    def step(self, imu: IMUPacket, gnss: Optional[GNSSPacket] = None, simulate_outage: bool = False) -> Dict[str, Any]:
        """Process one telemetry time-step."""
        # Calculate dt with protection against backward timestamp or spikes
        if self.last_imu_timestamp is None:
            dt = 0.02
        else:
            raw_dt = imu.timestamp - self.last_imu_timestamp
            dt = 0.02 if (raw_dt <= 0.0 or raw_dt > 0.5) else raw_dt
        self.last_imu_timestamp = imu.timestamp

        # Add to IMU sliding buffer
        sample = np.array([
            imu.accel_x, imu.accel_y, imu.accel_z,
            imu.gyro_x, imu.gyro_y, imu.gyro_z
        ], dtype=np.float32)
        self.imu_buffer.append(sample)

        # -------------------------------------------------------------
        # 1. Update Naive Baseline Dead Reckoning (to illustrate drift!)
        # -------------------------------------------------------------
        self.naive_yaw += imu.gyro_z * dt
        self.naive_vel = max(0.0, self.naive_vel + imu.accel_x * dt)
        self.naive_east += self.naive_vel * math.cos(self.naive_yaw) * dt
        self.naive_north += self.naive_vel * math.sin(self.naive_yaw) * dt

        # -------------------------------------------------------------
        # 2. Intelligent EKF Prediction Step
        # -------------------------------------------------------------
        self.ekf.predict(dt=dt, accel_fwd=imu.accel_x, gyro_yaw_rate=imu.gyro_z)

        # -------------------------------------------------------------
        # 3. Intelligent Deep Learning Feature Inference
        # -------------------------------------------------------------
        if len(self.imu_buffer) >= self.window_size:
            window_arr = np.array(self.imu_buffer)
            pred_v, var_v, pred_yr, var_yr = self.run_ml_inference(window_arr)
        else:
            pred_v = self.ekf.x[2]
            var_v = 0.5
            pred_yr = imu.gyro_z
            var_yr = 0.02

        # Determine whether GNSS outage is active
        # An outage occurs if:
        # 1. simulate_outage is True (e.g. tunnel window in simulation), OR
        # 2. self.force_outage is True (manual switch toggle), OR
        # 3. GPS was active but hasn't arrived for > 1.8s
        time_since_gnss = (imu.timestamp - self.last_gnss_timestamp) if self.last_gnss_timestamp is not None else 0.0
        gps_timed_out = (self.last_gnss_timestamp is not None and time_since_gnss > 1.8)
        
        is_outage = simulate_outage or self.force_outage or gps_timed_out

        calib_stats = {}
        if gnss is not None and not (simulate_outage or self.force_outage):
            # Active GNSS Mode: Transform GPS Lat/Lon to Local ENU
            is_outage = False
            gps_e, gps_n, _ = self.transformer.geodetic_to_enu(
                gnss.latitude, gnss.longitude, gnss.altitude or 0.0
            )

            # Course over ground in radians
            bearing_rad = math.radians(gnss.bearing_deg) if gnss.bearing_deg is not None else None

            # Calculate GNSS bearing rate for online calibrator
            bearing_rate = None
            if bearing_rad is not None:
                if self.last_gnss_bearing is not None and self.last_gnss_timestamp is not None:
                    gnss_dt = gnss.timestamp - self.last_gnss_timestamp
                    if 0.2 <= gnss_dt <= 3.0:
                        db = (bearing_rad - self.last_gnss_bearing + math.pi) % (2.0 * math.pi) - math.pi
                        bearing_rate = db / gnss_dt
                self.last_gnss_bearing = bearing_rad

            self.last_gnss_timestamp = gnss.timestamp

            # Check if vehicle is stationary for ZUPT
            if gnss.speed_ms is not None:
                is_stationary = gnss.speed_ms < 0.25
            else:
                is_stationary = (pred_v < 0.15) and (abs(imu.gyro_z) < 0.02)

            # Online Runtime Self-Correction / Drift Adaptation
            calib_stats = self.calibrator.calibrate_step(
                predicted_vel=pred_v,
                predicted_yaw_rate=pred_yr,
                gps_speed=gnss.speed_ms,
                gps_bearing_rate=bearing_rate,
                gps_accuracy_m=gnss.accuracy_m or 3.0,
                is_stationary=is_stationary
            )

            if is_stationary:
                self.ekf.update_zupt(measured_yaw_rate=imu.gyro_z)
                self.naive_vel = 0.0

            # EKF updates with authoritative GNSS observations
            self.ekf.update_gnss(
                east=gps_e,
                north=gps_n,
                speed=gnss.speed_ms,
                bearing_rad=bearing_rad,
                pos_accuracy_m=gnss.accuracy_m or 3.0
            )
            # Sync naive DR during active GPS so drift accumulates strictly from outage start
            self.naive_east = gps_e
            self.naive_north = gps_n
            self.naive_vel = gnss.speed_ms if gnss.speed_ms is not None else self.naive_vel
            if bearing_rad is not None:
                self.naive_yaw = bearing_rad

        elif is_outage:
            # -------------------------------------------------------------
            # Outage Mode (Tunnel / Urban Canyon): Dead Reckoning with ML!
            # -------------------------------------------------------------
            self.ekf.mark_outage(dt)

            # Apply online-learned device corrections to ML predictions
            calib_v, calib_yr = self.calibrator.apply_correction(pred_v, pred_yr)

            # EKF measurement update using ML drift-corrected speed and yaw rate
            self.ekf.update_ml_prediction(
                predicted_velocity=calib_v,
                predicted_yaw_rate=calib_yr,
                var_velocity=var_v,
                var_yaw_rate=var_yr,
                dt=dt,
                measured_gyro_yaw_rate=imu.gyro_z
            )
        else:
            # Normal sub-second inertial propagation between 1 Hz GNSS fixes:
            # EKF kinematic state was already updated by self.ekf.predict(dt)
            pass

        # -------------------------------------------------------------
        # 5. Geodetic Projection (ENU -> WGS84 Lat, Lon)
        # -------------------------------------------------------------
        ekf_state = self.ekf.get_state()
        est_lat, est_lon, _ = self.transformer.enu_to_geodetic(
            ekf_state["east_m"], ekf_state["north_m"]
        )
        naive_lat, naive_lon, _ = self.transformer.enu_to_geodetic(
            self.naive_east, self.naive_north
        )

        drift_distance_m = math.sqrt(
            (ekf_state["east_m"] - self.naive_east) ** 2 +
            (ekf_state["north_m"] - self.naive_north) ** 2
        )

        return {
            "timestamp": imu.timestamp,
            "outage_active": is_outage,
            "outage_duration_s": ekf_state["outage_duration_s"],
            # Intelligent EKF / AI Estimates
            "estimated_lat": est_lat,
            "estimated_lon": est_lon,
            "velocity_ms": ekf_state["velocity_ms"],
            "velocity_kmh": ekf_state["velocity_ms"] * 3.6,
            "heading_deg": ekf_state["yaw_deg"],
            "gyro_bias_rads": ekf_state["yaw_bias_rads"],
            "pos_uncertainty_m": ekf_state["pos_uncertainty_m"],
            # Naive IMU baseline
            "naive_lat": naive_lat,
            "naive_lon": naive_lon,
            "naive_vel_kmh": self.naive_vel * 3.6,
            "drift_error_m": drift_distance_m,
            # ML Model & Online Self-Correction Telemetry
            "ml_pred_vel_ms": pred_v,
            "ml_pred_yaw_rate_degs": math.degrees(pred_yr),
            "calibration_profile": self.calibrator.get_profile(),
            "calibration_update": calib_stats
        }

# Global singleton navigation engine
core = NavigationCore()

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    """Interactive Real-time Visual Demonstration Dashboard."""
    html_file = os.path.join(os.path.dirname(__file__), "dashboard.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>SIH26168 Intelligent Dead Reckoning Backend Running</h1>"

@app.post("/api/telemetry/feed")
def feed_telemetry(payload: TelemetryFeedRequest):
    """Ingest single sensor packet."""
    result = core.step(payload.imu, payload.gnss, payload.simulate_outage)
    return result

@app.post("/api/simulation/toggle_outage")
def toggle_outage(payload: OutageToggleRequest):
    """Toggle simulated GNSS outage (enter/exit tunnel)."""
    core.force_outage = payload.outage_active
    return {"status": "success", "force_outage": core.force_outage}

@app.post("/api/simulation/reset")
def reset_simulation():
    """Reset the navigation core and simulation states."""
    core.reset()
    return {"status": "success", "message": "Navigation engine reset complete"}

@app.get("/api/status")
def get_status():
    """Retrieve system diagnostics, device profile, and GPU status."""
    gpu_available = False
    gpu_name = "N/A"
    try:
        import torch
        gpu_available = torch.cuda.is_available()
        if gpu_available:
            gpu_name = torch.cuda.get_device_name(0)
    except Exception:
        pass

    return {
        "system": "SIH26168 AI-ML Intelligent Dead Reckoning",
        "gpu_available": gpu_available,
        "gpu_device": gpu_name,
        "model_loaded": core.model is not None or core.onnx_session is not None,
        "force_outage": core.force_outage,
        "calibration_profile": core.calibrator.get_profile(),
        "current_ekf_state": core.ekf.get_state()
    }

@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """
    WebSocket endpoint for real-time streaming telemetry and bidirectional control.
    Uses asynchronous task delegation so controls (outage toggle, reset) work smoothly mid-stream.
    """
    await websocket.accept()
    print("[WS] Client connected")
    sim_task: Optional[asyncio.Task] = None

    async def run_simulation_stream(sim_dur: float, outage_s: float, outage_e: float):
        try:
            core.reset()
            gen = VehicularTrajectoryGenerator(sampling_rate_hz=50.0)
            sim_data = gen.generate_synthetic_drive(
                duration_sec=sim_dur,
                outage_windows=[(outage_s, outage_e)]
            )
            step_skip = 2  # send every 2nd sample for smooth 25fps web rendering
            total_len = len(sim_data["time"])

            for i in range(0, total_len, step_skip):
                t = float(sim_data["time"][i])
                imu_p = IMUPacket(
                    timestamp=t,
                    accel_x=float(sim_data["accel_x"][i]),
                    accel_y=float(sim_data["accel_y"][i]),
                    accel_z=float(sim_data["accel_z"][i]),
                    gyro_x=float(sim_data["gyro_x"][i]),
                    gyro_y=float(sim_data["gyro_y"][i]),
                    gyro_z=float(sim_data["gyro_z"][i])
                )

                gnss_p = None
                if sim_data["gps_mask"][i]:
                    g_lat, g_lon, _ = core.transformer.enu_to_geodetic(
                        sim_data["gps_east"][i], sim_data["gps_north"][i]
                    )
                    gnss_p = GNSSPacket(
                        timestamp=t,
                        latitude=g_lat,
                        longitude=g_lon,
                        speed_ms=float(sim_data["gps_speed"][i]),
                        bearing_deg=float(math.degrees(sim_data["gps_bearing"][i]) % 360.0),
                        accuracy_m=2.0
                    )

                gt_lat, gt_lon, _ = core.transformer.enu_to_geodetic(
                    sim_data["gt_east"][i], sim_data["gt_north"][i]
                )

                is_sim_outage = bool(sim_data["in_outage"][i]) if "in_outage" in sim_data else False
                res = core.step(imu_p, gnss_p, simulate_outage=is_sim_outage)
                res["gt_lat"] = gt_lat
                res["gt_lon"] = gt_lon
                res["gt_speed_kmh"] = float(sim_data["gt_speed"][i] * 3.6)
                res["tunnel_window"] = [outage_s, outage_e]

                await websocket.send_json(res)
                await asyncio.sleep(0.02)  # smooth 50fps pacing
        except asyncio.CancelledError:
            pass
        except Exception as err:
            print(f"[WS Sim Error] {err}")

    try:
        while True:
            data = await websocket.receive_json()
            cmd = data.get("command")
            if cmd == "start_simulation":
                if sim_task and not sim_task.done():
                    sim_task.cancel()
                sim_dur = float(data.get("duration", 150.0))
                outage_s = float(data.get("outage_start", 45.0))
                outage_e = float(data.get("outage_end", 95.0))
                sim_task = asyncio.create_task(run_simulation_stream(sim_dur, outage_s, outage_e))

            elif cmd == "toggle_outage":
                val = bool(data.get("value", not core.force_outage))
                core.force_outage = val
                await websocket.send_json({"event": "outage_toggled", "force_outage": core.force_outage})

            elif cmd == "reset":
                if sim_task and not sim_task.done():
                    sim_task.cancel()
                core.reset()
                await websocket.send_json({"event": "reset_complete"})

    except WebSocketDisconnect:
        if sim_task and not sim_task.done():
            sim_task.cancel()
        print("[WS] Client disconnected")
    except Exception as e:
        if sim_task and not sim_task.done():
            sim_task.cancel()
        print(f"[WS Error] {e}")
