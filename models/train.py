import os
import sys
import time
import math
import numpy as np
import torch
import torch.nn as nn
from typing import Optional, List, Tuple, Dict, Any
from torch.utils.data import Dataset, DataLoader

# Add parent path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.dataset_generator import VehicularTrajectoryGenerator
from data.iovnbd_loader import IOVNBDLoader
from models.idr_model import IntelligentDeadReckoningNet, HeteroscedasticLoss

class IMUSlidingWindowDataset(Dataset):
    """
    Sliding window dataset for vehicular IMU time-series.
    Input: (Window_Length, 6) -> [ax, ay, az, gx, gy, gz]
    Targets: [target_speed_ms, target_yaw_rate_rads]
    """
    def __init__(self, trajectories: list, window_size: int = 50, step: int = 5):
        self.windows = []
        self.targets_speed = []
        self.targets_yaw_rate = []

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

            for i in range(0, n_samples - window_size + 1, step):
                win = imu_matrix[i : i + window_size]
                # Target is the vehicle state at the end of the observation window
                self.windows.append(win)
                self.targets_speed.append(gt_spd[i + window_size - 1])
                self.targets_yaw_rate.append(gt_yr[i + window_size - 1])

        self.windows = np.array(self.windows, dtype=np.float32)
        self.targets_speed = np.array(self.targets_speed, dtype=np.float32)
        self.targets_yaw_rate = np.array(self.targets_yaw_rate, dtype=np.float32)

    def __len__(self):
        return len(self.windows)

    def __getitem__(self, idx):
        return (
            torch.from_numpy(self.windows[idx]),
            torch.tensor(self.targets_speed[idx], dtype=torch.float32),
            torch.tensor(self.targets_yaw_rate[idx], dtype=torch.float32)
        )

def generate_multi_trajectory_dataset(n_runs: int = 8, fs: float = 50.0) -> list:
    """Generate multiple realistic training drives with distinct biases and vibrations."""
    trajectories = []
    generator = VehicularTrajectoryGenerator(sampling_rate_hz=fs, seed=100)
    for i in range(n_runs):
        duration = float(np.random.uniform(120.0, 240.0))
        accel_b = float(np.random.uniform(0.02, 0.15))
        gyro_b = float(np.random.uniform(-0.04, 0.04))
        vibe_amp = float(np.random.uniform(0.1, 0.4))
        tilt = float(np.random.uniform(-8.0, 8.0))

        traj = generator.generate_synthetic_drive(
            duration_sec=duration,
            accel_bias=accel_b,
            gyro_bias=gyro_b,
            vibration_amp=vibe_amp,
            tilt_pitch_deg=tilt
        )
        trajectories.append(traj)
    return trajectories

def train_idr_model(
    epochs: int = 25,
    batch_size: int = 64,
    window_size: int = 50,
    lr: float = 1e-3,
    save_path: str = "idr_model_best.pt",
    onnx_path: str = "idr_model.onnx",
    data_dir: Optional[str] = None,
    dataset_mode: str = "auto",
    target_fs: float = 50.0,
    device_name: Optional[str] = None
):
    print("=" * 60)
    print("AI-ML Intelligent Dead Reckoning (IDR) Training Pipeline")
    print("Target Problem: SIH26168 - GNSS Signal Loss in Tunnels & Canyons")
    print(f"Dataset Mode: {dataset_mode.upper()} | Target Fs: {target_fs} Hz")
    print("=" * 60)

    # Device configuration with GPU acceleration support
    if device_name is not None:
        device = torch.device(device_name)
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if device.type == "cuda":
        try:
            # Test small tensor operation to verify kernel availability (e.g. sm_120 vs sm_90)
            t_test = torch.zeros(1, device="cuda")
            _ = t_test + 1
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"[Device] Using compute device: {device} ({gpu_name}, {gpu_mem:.2f} GB VRAM)")
            torch.backends.cudnn.benchmark = True
        except Exception as e:
            print(f"[Device Notice] GPU detected but CUDA kernels unavailable for this architecture ({e}). Falling back to optimized CPU execution.")
            device = torch.device("cpu")
    else:
        print("[Device] Using compute device: cpu")

    # 1. Ingest IO-VNBD or Generate Synthetic Data
    iovnbd_trajs = []
    found_dir = None
    loader = IOVNBDLoader(default_fs=10.0)

    candidate_dirs = []
    if data_dir:
        candidate_dirs.append(data_dir)
    candidate_dirs.extend(["data/iovnbd", "data/iovnbd_samples", "data"])

    if dataset_mode in ("auto", "iovnbd", "hybrid"):
        for cdir in candidate_dirs:
            if os.path.isdir(cdir):
                loaded = loader.load_directory(cdir, target_fs=target_fs)
                if loaded:
                    iovnbd_trajs = loaded
                    found_dir = cdir
                    break

    train_trajs = []
    val_trajs = []

    if dataset_mode == "iovnbd" and not iovnbd_trajs:
        raise FileNotFoundError(
            f"dataset_mode='iovnbd' requested, but no valid IO-VNBD CSV logs found in candidate dirs: {candidate_dirs}"
        )

    if iovnbd_trajs:
        print(f"[Data: IO-VNBD] Loaded {len(iovnbd_trajs)} real vehicular log(s) from '{found_dir}'.")
        if len(iovnbd_trajs) >= 2:
            n_val = max(1, int(len(iovnbd_trajs) * 0.2))
            val_trajs.extend(iovnbd_trajs[-n_val:])
            train_trajs.extend(iovnbd_trajs[:-n_val])
        else:
            # Single trajectory: split sequentially 80% train, 20% val
            t_full = iovnbd_trajs[0]
            n_total = len(t_full["time"])
            split_idx = int(n_total * 0.8)
            traj_train = {k: v[:split_idx] if isinstance(v, np.ndarray) and len(v) == n_total else v for k, v in t_full.items()}
            traj_val = {k: v[split_idx:] if isinstance(v, np.ndarray) and len(v) == n_total else v for k, v in t_full.items()}
            train_trajs.append(traj_train)
            val_trajs.append(traj_val)

        if dataset_mode == "hybrid":
            print("[Data: Hybrid] Combining IO-VNBD logs with domain-randomized synthetic drives...")
            synth_train = generate_multi_trajectory_dataset(n_runs=4, fs=target_fs)
            synth_val = generate_multi_trajectory_dataset(n_runs=1, fs=target_fs)
            train_trajs.extend(synth_train)
            val_trajs.extend(synth_val)
    else:
        print("[Data: Synthetic] No external IO-VNBD logs detected. Seamlessly using high-fidelity vehicular simulator.")
        train_trajs = generate_multi_trajectory_dataset(n_runs=8, fs=target_fs)
        val_trajs = generate_multi_trajectory_dataset(n_runs=2, fs=target_fs)

    train_dataset = IMUSlidingWindowDataset(train_trajs, window_size=window_size, step=10)
    val_dataset = IMUSlidingWindowDataset(val_trajs, window_size=window_size, step=15)

    print(f"[Data] Train Windows: {len(train_dataset)} | Validation Windows: {len(val_dataset)}")

    if len(train_dataset) == 0:
        raise ValueError(
            f"No training windows could be generated with window_size={window_size}. "
            "Ensure the provided trajectories contain sufficient duration (> window_size samples)."
        )
    if len(val_dataset) == 0:
        print("[Data Notice] Validation set has 0 windows. Using training subset for validation metrics.")
        val_dataset = train_dataset

    effective_batch = min(batch_size, max(1, len(train_dataset)))
    train_loader = DataLoader(
        train_dataset,
        batch_size=effective_batch,
        shuffle=True,
        drop_last=(len(train_dataset) >= effective_batch),
        pin_memory=(device.type == "cuda")
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=min(batch_size, max(1, len(val_dataset))),
        shuffle=False,
        pin_memory=(device.type == "cuda")
    )

    # 2. Instantiate Model and Loss
    try:
        model = IntelligentDeadReckoningNet(
            in_channels=6,
            conv_channels=64,
            gru_hidden_size=64,
            gru_layers=2,
            dropout=0.15
        ).to(device)
    except Exception as e:
        print(f"[Model Init Notice] Falling back to CPU for model layers: {e}")
        device = torch.device("cpu")
        model = IntelligentDeadReckoningNet(
            in_channels=6,
            conv_channels=64,
            gru_hidden_size=64,
            gru_layers=2,
            dropout=0.15
        ).to(device)

    loss_fn = HeteroscedasticLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    best_val_loss = float("inf")
    start_time = time.time()

    # 3. Training Loop
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss_total = 0.0
        train_speed_mae = 0.0
        train_yaw_mae = 0.0
        batch_count = 0

        for x_win, target_speed, target_yaw in train_loader:
            x_win = x_win.to(device)
            target_speed = target_speed.to(device)
            target_yaw = target_yaw.to(device)

            optimizer.zero_grad()

            pred_vel, pred_vel_var, pred_yaw, pred_yaw_var = model(x_win)

            loss_vel = loss_fn(pred_vel, pred_vel_var, target_speed)
            loss_yaw = loss_fn(pred_yaw, pred_yaw_var, target_yaw)
            total_loss = loss_vel + 2.0 * loss_yaw

            total_loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()

            train_loss_total += total_loss.item()
            train_speed_mae += torch.mean(torch.abs(pred_vel - target_speed)).item()
            train_yaw_mae += torch.mean(torch.abs(pred_yaw - target_yaw)).item()
            batch_count += 1

        scheduler.step()

        # Validation
        model.eval()
        val_loss_total = 0.0
        val_speed_mae = 0.0
        val_yaw_mae = 0.0
        val_batches = 0

        with torch.no_grad():
            for x_win, target_speed, target_yaw in val_loader:
                x_win = x_win.to(device)
                target_speed = target_speed.to(device)
                target_yaw = target_yaw.to(device)

                pred_vel, pred_vel_var, pred_yaw, pred_yaw_var = model(x_win)

                loss_vel = loss_fn(pred_vel, pred_vel_var, target_speed)
                loss_yaw = loss_fn(pred_yaw, pred_yaw_var, target_yaw)
                total_loss = loss_vel + 2.0 * loss_yaw

                val_loss_total += total_loss.item()
                val_speed_mae += torch.mean(torch.abs(pred_vel - target_speed)).item()
                val_yaw_mae += torch.mean(torch.abs(pred_yaw - target_yaw)).item()
                val_batches += 1

        avg_train_loss = train_loss_total / max(1, batch_count)
        avg_val_loss = val_loss_total / max(1, val_batches)
        avg_val_speed_mae = val_speed_mae / max(1, val_batches)
        avg_val_yaw_mae = val_yaw_mae / max(1, val_batches)

        # Print progress
        if epoch % 5 == 0 or epoch == 1 or epoch == epochs:
            print(
                f"Epoch [{epoch:02d}/{epochs:02d}] "
                f"Train Loss: {avg_train_loss:.4f} | "
                f"Val Loss: {avg_val_loss:.4f} | "
                f"Val Speed MAE: {avg_val_speed_mae:.3f} m/s | "
                f"Val Yaw MAE: {math.degrees(avg_val_yaw_mae):.3f} deg/s"
            )

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "val_loss": best_val_loss,
                    "val_speed_mae": avg_val_speed_mae,
                    "val_yaw_mae": avg_val_yaw_mae,
                    "window_size": window_size,
                    "in_channels": 6
                },
                save_path
            )

    elapsed = time.time() - start_time
    print(f"[Training Complete] Finished in {elapsed:.2f}s. Best Val Loss: {best_val_loss:.4f}")
    print(f"[Model Saved] Saved best weights to {save_path}")

    # 4. Export to TorchScript & ONNX for Edge / Mobile Deployment
    model.eval()
    dummy_input = torch.randn(1, window_size, 6, device=device)

    # TorchScript (PyTorch Mobile ready)
    script_path = "idr_model_scripted.pt"
    try:
        traced_model = torch.jit.trace(model, dummy_input)
        traced_model.save(script_path)
        print(f"[Export Success] TorchScript edge model exported: {script_path} ({os.path.getsize(script_path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"[TorchScript Export Notice] {e}")

    # ONNX export
    try:
        print(f"[Export] Exporting model to ONNX format: {onnx_path}...")
        torch.onnx.export(
            model,
            dummy_input,
            onnx_path,
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=["imu_window"],
            output_names=["speed_mean", "speed_var", "yaw_rate_mean", "yaw_rate_var"],
            dynamic_axes={
                "imu_window": {0: "batch_size"},
                "speed_mean": {0: "batch_size"},
                "speed_var": {0: "batch_size"},
                "yaw_rate_mean": {0: "batch_size"},
                "yaw_rate_var": {0: "batch_size"},
            }
        )
        print(f"[Export Success] ONNX model exported: {onnx_path} ({os.path.getsize(onnx_path) / 1024:.1f} KB)")
    except Exception as e:
        print(f"[ONNX Export Notice] Optional ONNX export skipped ({e}). TorchScript model available at {script_path}.")

    return model, save_path, onnx_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI-ML Intelligent Dead Reckoning Training Pipeline (SIH26168)")
    parser.add_argument("--epochs", type=int, default=20, help="Number of training epochs (default: 20)")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size (default: 64)")
    parser.add_argument("--window-size", type=int, default=50, help="Sliding window length (default: 50)")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate (default: 1e-3)")
    parser.add_argument("--data-dir", type=str, default=None, help="Directory containing IO-VNBD dataset CSV logs")
    parser.add_argument("--dataset-mode", type=str, default="auto", choices=["auto", "iovnbd", "synthetic", "hybrid"], help="Dataset source mode (default: auto)")
    parser.add_argument("--save-path", type=str, default="idr_model_best.pt", help="Best weights checkpoint destination")
    parser.add_argument("--device", type=str, default=None, help="Explicit compute device (e.g. cpu, cuda)")
    args = parser.parse_args()

    train_idr_model(
        epochs=args.epochs,
        batch_size=args.batch_size,
        window_size=args.window_size,
        lr=args.lr,
        save_path=args.save_path,
        data_dir=args.data_dir,
        dataset_mode=args.dataset_mode,
        device_name=args.device
    )
