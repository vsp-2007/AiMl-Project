"""
IO-VNBD Benchmark & Outage Evaluation Suite.

Target Problem: SIH26168 - AI-ML based Intelligent Dead Reckoning System
Evaluates IntelligentDeadReckoningNet + IntelligentEKF against Pure IMU Dead Reckoning
on IO-VNBD vehicular trajectories during simulated GNSS outages (tunnels, urban canyons).
"""

import os
import sys
import math
import json
import argparse
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
import torch

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.idr_model import IntelligentDeadReckoningNet
from sensor_fusion.ekf import IntelligentEKF, normalize_angle
from data.iovnbd_loader import IOVNBDLoader, generate_sample_iovnbd_v_csv


def evaluate_trajectory_outage(
    model: IntelligentDeadReckoningNet,
    trajectory: Dict[str, np.ndarray],
    outage_start_sec: float = 20.0,
    outage_duration_sec: float = 30.0,
    window_size: int = 50,
    device: Optional[torch.device] = None,
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Evaluates Dead Reckoning during a simulated GNSS outage on a vehicular trajectory.

    Compares:
    1. Baseline: Pure IMU kinematic integration (uncorrected forward dead reckoning).
    2. Intelligent Dead Reckoning: Hybrid CNN-GRU inference fused with 5-state IntelligentEKF.

    Returns:
        Comprehensive metric dictionary including drift MAE, max drift, and reduction factor.
    """
    model.eval()
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = torch.device("cpu")
    else:
        model.to(device)

    rng = np.random.RandomState(seed if seed is not None else 42)
    t = trajectory["time"]
    dt = trajectory["dt"]
    n_steps = len(t)

    outage_end_sec = outage_start_sec + outage_duration_sec
    outage_indices = np.where((t >= outage_start_sec) & (t <= outage_end_sec))[0]

    if len(outage_indices) < 2:
        raise ValueError(
            f"Outage window [{outage_start_sec}, {outage_end_sec}] contains fewer than 2 samples in trajectory of duration {t[-1]:.1f}s."
        )

    # Ground truth
    gt_east = trajectory["gt_east"]
    gt_north = trajectory["gt_north"]
    gt_speed = trajectory["gt_speed"]
    gt_yaw = trajectory["gt_yaw"]
    gt_yaw_rate = trajectory["gt_yaw_rate"]

    # Sensor signals
    ax = trajectory["accel_x"]
    ay = trajectory["accel_y"]
    az = trajectory["accel_z"]
    gx = trajectory["gyro_x"]
    gy = trajectory["gyro_y"]
    gz = trajectory["gyro_z"]

    # Calculate distance traveled during outage
    speed_in_outage = gt_speed[outage_indices]
    distance_traveled_m = float(np.sum(speed_in_outage) * dt)

    # -------------------------------------------------------------
    # 1. Baseline: Pure IMU Kinematic Integration
    # -------------------------------------------------------------
    base_east = np.zeros(n_steps)
    base_north = np.zeros(n_steps)
    base_speed = np.zeros(n_steps)
    base_yaw = np.zeros(n_steps)

    base_east[0] = gt_east[0]
    base_north[0] = gt_north[0]
    base_speed[0] = gt_speed[0]
    base_yaw[0] = gt_yaw[0]

    for k in range(1, n_steps):
        time_k = t[k]
        in_outage = (outage_start_sec <= time_k <= outage_end_sec)

        if not in_outage:
            # When GNSS is available, reset baseline to GNSS fix
            base_east[k] = gt_east[k]
            base_north[k] = gt_north[k]
            base_speed[k] = gt_speed[k]
            base_yaw[k] = gt_yaw[k]
        else:
            # During GNSS loss: pure uncorrected Euler kinematic integration
            # v = v + a_x * dt
            base_speed[k] = max(0.0, base_speed[k - 1] + ax[k] * dt)
            # yaw = yaw + omega_z * dt
            base_yaw[k] = normalize_angle(base_yaw[k - 1] + gz[k] * dt)
            # pos = pos + v * dir * dt
            base_east[k] = base_east[k - 1] + base_speed[k] * math.cos(base_yaw[k]) * dt
            base_north[k] = base_north[k - 1] + base_speed[k] * math.sin(base_yaw[k]) * dt

    # -------------------------------------------------------------
    # 2. Intelligent Dead Reckoning: CNN-GRU + 5-State EKF
    # -------------------------------------------------------------
    ekf = IntelligentEKF(
        init_east=float(gt_east[0]),
        init_north=float(gt_north[0]),
        init_velocity=float(gt_speed[0]),
        init_yaw_rad=float(gt_yaw[0]),
        q_pos=0.04,
        q_vel=0.15,
        q_yaw=0.01,
        q_bias=1e-4
    )

    ekf_east = np.zeros(n_steps)
    ekf_north = np.zeros(n_steps)
    ekf_speed = np.zeros(n_steps)
    ekf_yaw = np.zeros(n_steps)

    pred_speeds = np.zeros(n_steps)
    pred_yaw_rates = np.zeros(n_steps)

    # Pre-build IMU matrix for window slicing: (n_steps, 6)
    imu_matrix = np.column_stack([ax, ay, az, gx, gy, gz]).astype(np.float32)

    with torch.no_grad():
        for k in range(n_steps):
            time_k = t[k]
            in_outage = (outage_start_sec <= time_k <= outage_end_sec)

            # EKF State Prediction using IMU step
            ekf.predict(dt=dt, accel_fwd=float(ax[k]), gyro_yaw_rate=float(gz[k]))

            # Intelligent Neural Network Inference
            if k >= window_size:
                win_tensor = torch.from_numpy(imu_matrix[k - window_size : k]).unsqueeze(0).to(device)
                pred_v, pred_v_var, pred_w, pred_w_var = model(win_tensor)

                v_val = float(pred_v.squeeze().cpu().item())
                v_var = float(pred_v_var.squeeze().cpu().item())
                w_val = float(pred_w.squeeze().cpu().item())
                w_var = float(pred_w_var.squeeze().cpu().item())

                pred_speeds[k] = v_val
                pred_yaw_rates[k] = w_val
            else:
                v_val = float(gt_speed[k])
                v_var = 0.1
                w_val = float(gz[k])
                w_var = 0.05
                pred_speeds[k] = v_val
                pred_yaw_rates[k] = w_val

            if not in_outage:
                # GNSS Available: update position and velocity
                # Simulated GNSS noise ~ 1.5m
                noisy_east = float(gt_east[k] + rng.normal(0, 0.5))
                noisy_north = float(gt_north[k] + rng.normal(0, 0.5))
                noisy_spd = float(max(0.0, gt_speed[k] + rng.normal(0, 0.2)))
                noisy_hdg = float(normalize_angle(gt_yaw[k] + rng.normal(0, 0.05)))

                ekf.update_gnss(
                    east=noisy_east,
                    north=noisy_north,
                    speed=noisy_spd,
                    bearing_rad=noisy_hdg,
                    pos_accuracy_m=2.0,
                    speed_accuracy_ms=0.3,
                    bearing_accuracy_rad=0.08
                )
            else:
                # GNSS Outage: Intelligent Neural Innovation Update
                # Fuses ML velocity and yaw rate predictions to bound drift
                ekf.update_ml_prediction(
                    predicted_velocity=v_val,
                    predicted_yaw_rate=w_val,
                    var_velocity=max(1e-4, v_var),
                    var_yaw_rate=max(1e-4, w_var),
                    dt=dt,
                    measured_gyro_yaw_rate=float(gz[k])
                )

            # Zero-Velocity Update (ZUPT) if detected stationary
            if v_val < 0.15 and abs(gz[k]) < 0.03:
                ekf.update_zupt(float(gz[k]))

            state = ekf.get_state()
            ekf_east[k] = state["east_m"]
            ekf_north[k] = state["north_m"]
            ekf_speed[k] = state["velocity_ms"]
            ekf_yaw[k] = state["yaw_rad"]

    # -------------------------------------------------------------
    # 3. Compute Outage Error Metrics
    # -------------------------------------------------------------
    # Position errors over outage
    base_pos_err = np.sqrt(
        (base_east[outage_indices] - gt_east[outage_indices]) ** 2
        + (base_north[outage_indices] - gt_north[outage_indices]) ** 2
    )
    ekf_pos_err = np.sqrt(
        (ekf_east[outage_indices] - gt_east[outage_indices]) ** 2
        + (ekf_north[outage_indices] - gt_north[outage_indices]) ** 2
    )

    # Speed errors
    base_spd_err = np.abs(base_speed[outage_indices] - gt_speed[outage_indices])
    ekf_spd_err = np.abs(ekf_speed[outage_indices] - gt_speed[outage_indices])
    ml_spd_err = np.abs(pred_speeds[outage_indices] - gt_speed[outage_indices])

    # Yaw rate errors
    ml_yr_err = np.abs(pred_yaw_rates[outage_indices] - gt_yaw_rate[outage_indices])

    base_max_drift = float(np.max(base_pos_err))
    ekf_max_drift = float(np.max(ekf_pos_err))
    drift_reduction_ratio = (base_max_drift / max(1e-3, ekf_max_drift)) if ekf_max_drift > 0 else 1.0

    return {
        "outage_start_sec": outage_start_sec,
        "outage_duration_sec": outage_duration_sec,
        "distance_traveled_m": distance_traveled_m,
        "baseline_pure_imu": {
            "position_drift_mae_m": float(np.mean(base_pos_err)),
            "position_drift_max_m": base_max_drift,
            "position_drift_final_m": float(base_pos_err[-1]),
            "relative_drift_percent": float((base_max_drift / max(1.0, distance_traveled_m)) * 100.0),
            "speed_mae_ms": float(np.mean(base_spd_err))
        },
        "intelligent_dead_reckoning": {
            "position_drift_mae_m": float(np.mean(ekf_pos_err)),
            "position_drift_max_m": ekf_max_drift,
            "position_drift_final_m": float(ekf_pos_err[-1]),
            "relative_drift_percent": float((ekf_max_drift / max(1.0, distance_traveled_m)) * 100.0),
            "speed_mae_ms": float(np.mean(ekf_spd_err)),
            "ml_model_speed_mae_ms": float(np.mean(ml_spd_err)),
            "ml_model_yaw_rate_mae_degs": float(math.degrees(np.mean(ml_yr_err)))
        },
        "drift_reduction_ratio": float(drift_reduction_ratio),
        "percentage_improvement": float(max(0.0, (1.0 - ekf_max_drift / max(1e-4, base_max_drift)) * 100.0))
    }


def print_benchmark_table(metrics: Dict[str, Any], title: str = "IO-VNBD GNSS Outage Benchmark"):
    """Prints a structured comparison report table."""
    base = metrics["baseline_pure_imu"]
    idr = metrics["intelligent_dead_reckoning"]

    print("\n" + "=" * 76)
    print(f"  {title.upper()}")
    print("  Problem Statement: SIH26168 - AI-ML Intelligent Dead Reckoning")
    print("=" * 76)
    print(f"  Outage Duration:     {metrics['outage_duration_sec']:.1f} seconds (from t={metrics['outage_start_sec']:.1f}s)")
    print(f"  Distance Traveled:   {metrics['distance_traveled_m']:.2f} meters")
    print("-" * 76)
    print(f"  {'Metric':<32} | {'Pure IMU Baseline':<18} | {'Intelligent DR':<16}")
    print("-" * 76)
    print(f"  {'Position Drift MAE (m)':<32} | {base['position_drift_mae_m']:>15.2f} m  | {idr['position_drift_mae_m']:>13.2f} m")
    print(f"  {'Maximum Position Drift (m)':<32} | {base['position_drift_max_m']:>15.2f} m  | {idr['position_drift_max_m']:>13.2f} m")
    print(f"  {'Final Position Drift (m)':<32} | {base['position_drift_final_m']:>15.2f} m  | {idr['position_drift_final_m']:>13.2f} m")
    print(f"  {'Relative Drift (% dist)':<32} | {base['relative_drift_percent']:>15.2f} %  | {idr['relative_drift_percent']:>13.2f} %")
    print(f"  {'Speed Estimation MAE (m/s)':<32} | {base['speed_mae_ms']:>15.2f} m/s| {idr['speed_mae_ms']:>13.2f} m/s")
    print("-" * 76)
    print(f"  ML Neural Speed MAE:       {idr['ml_model_speed_mae_ms']:.3f} m/s")
    print(f"  ML Neural Yaw Rate MAE:    {idr['ml_model_yaw_rate_mae_degs']:.3f} deg/s")
    print(f"  >>> Drift Reduction Ratio: {metrics['drift_reduction_ratio']:.2f}x improvement")
    print(f"  >>> Accuracy Enhancement:  {metrics['percentage_improvement']:.2f}% error reduction")
    print("=" * 76 + "\n")


def run_iovnbd_benchmark(
    model_path: str = "idr_model_best.pt",
    data_path: Optional[str] = None,
    outage_start: float = 20.0,
    outage_duration: float = 30.0,
    window_size: int = 50,
    output_json: Optional[str] = None
) -> Dict[str, Any]:
    """Runs end-to-end evaluation on IO-VNBD dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = IntelligentDeadReckoningNet(in_channels=6, conv_channels=64, gru_hidden_size=64, gru_layers=2)

    if os.path.exists(model_path):
        try:
            ckpt = torch.load(model_path, map_location=device, weights_only=False)
            state_dict = ckpt["model_state_dict"] if "model_state_dict" in ckpt else ckpt
            model.load_state_dict(state_dict)
            print(f"[Model] Successfully loaded weights from {model_path}")
        except Exception as e:
            print(f"[Model Notice] Could not load checkpoint ({e}), evaluating model architecture.")
    else:
        print(f"[Model Notice] Checkpoint {model_path} not found. Running with initialized weights.")

    model.to(device)
    model.eval()

    # Determine data file
    loader = IOVNBDLoader(default_fs=10.0)
    csv_file = None

    if data_path and os.path.isfile(data_path):
        csv_file = data_path
    elif data_path and os.path.isdir(data_path):
        files = sorted([f for f in os.listdir(data_path) if f.endswith(".csv")])
        if files:
            csv_file = os.path.join(data_path, files[0])

    if csv_file is None:
        # Check standard sample directories
        for fallback_dir in ["data/iovnbd_samples", "data/iovnbd", "data"]:
            if os.path.isdir(fallback_dir):
                files = sorted([os.path.join(fallback_dir, f) for f in os.listdir(fallback_dir) if f.endswith(".csv")])
                if files:
                    csv_file = files[0]
                    break

    if csv_file is None:
        # Auto-generate a valid sample CSV adhering to IO-VNBD schema
        sample_path = "data/iovnbd_samples/V-Drive_Sample1.csv"
        print(f"[IO-VNBD] No existing CSV found. Auto-generating official-schema sample: {sample_path}")
        generate_sample_iovnbd_v_csv(sample_path, duration_sec=120.0)
        csv_file = sample_path

    print(f"[IO-VNBD] Loading vehicular trajectory from: {csv_file}")
    traj = loader.load_csv(csv_file, target_fs=50.0)

    # Adjust outage start if trajectory is short
    traj_duration = float(traj["time"][-1] - traj["time"][0])
    if traj_duration <= outage_start + outage_duration:
        outage_start = max(5.0, traj_duration * 0.2)
        outage_duration = max(5.0, traj_duration * 0.5)

    metrics = evaluate_trajectory_outage(
        model=model,
        trajectory=traj,
        outage_start_sec=outage_start,
        outage_duration_sec=outage_duration,
        window_size=window_size,
        device=device
    )

    print_benchmark_table(metrics, title=f"IO-VNBD Outage Benchmark ({os.path.basename(csv_file)})")

    if output_json:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"[Benchmark] Saved metrics JSON to {output_json}")

    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IO-VNBD Benchmark & GNSS Outage Evaluator (SIH26168)")
    parser.add_argument("--model-path", type=str, default="idr_model_best.pt", help="Path to trained IDR model checkpoint")
    parser.add_argument("--data-path", type=str, default=None, help="Path to IO-VNBD CSV log or folder")
    parser.add_argument("--outage-start", type=float, default=20.0, help="GNSS outage start timestamp in seconds")
    parser.add_argument("--outage-duration", type=float, default=30.0, help="GNSS outage duration in seconds")
    parser.add_argument("--window-size", type=int, default=50, help="IMU temporal window length")
    parser.add_argument("--output-json", type=str, default=None, help="Optional output JSON path for metrics")
    args = parser.parse_args()

    run_iovnbd_benchmark(
        model_path=args.model_path,
        data_path=args.data_path,
        outage_start=args.outage_start,
        outage_duration=args.outage_duration,
        window_size=args.window_size,
        output_json=args.output_json
    )
