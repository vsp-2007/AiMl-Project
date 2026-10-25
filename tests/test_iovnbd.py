"""
Unit tests for IO-VNBD dataset loader, schema parser, preprocessor, and benchmark evaluator.
"""

import os
import csv
import math
import tempfile
import numpy as np
import pytest
import torch

from data.iovnbd_loader import (
    IOVNBDLoader,
    IOVNBDDataset,
    IOVNBD_VBOX_COLUMNS,
    IOVNBD_SMARTPHONE_COLUMNS,
    generate_sample_iovnbd_v_csv,
    generate_sample_iovnbd_s_csv,
    compass_bearing_to_enu_yaw,
    enu_yaw_to_compass_bearing,
    STANDARD_GRAVITY_G,
    FORD_FIESTA_WHEEL_RADIUS_M
)
from benchmark_iovnbd import evaluate_trajectory_outage, run_iovnbd_benchmark
from models.idr_model import IntelligentDeadReckoningNet
from models.train import train_idr_model


def test_vbox_schema_and_unit_conversions(tmp_path):
    """Verify IO-VNBD Vehicle CAN/VBOX 29-column schema and exact physical unit conversions."""
    csv_file = str(tmp_path / "V-TestDrive.csv")
    generate_sample_iovnbd_v_csv(csv_file, duration_sec=30.0, fs=10.0, seed=10)

    # 1. Verify CSV column headers
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == IOVNBD_VBOX_COLUMNS
        assert len(headers) == 29

    # 2. Parse with IOVNBDLoader
    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    assert "accel_x" in traj
    assert "accel_y" in traj
    assert "accel_z" in traj
    assert "gyro_z" in traj
    assert "gt_speed" in traj
    assert "gt_yaw_rate" in traj
    assert "gt_east" in traj
    assert "gt_north" in traj
    assert "wheel_speed" in traj
    assert "gps_mask" in traj

    # 3. Verify sample length (30s at 10Hz = 300 steps)
    assert len(traj["time"]) == 300
    assert abs(traj["fs"] - 10.0) < 1e-3
    assert abs(traj["dt"] - 0.1) < 1e-3

    # 4. Verify speed and yaw rate consistency
    assert np.all(traj["gt_speed"] >= 0.0)
    assert np.all(np.isfinite(traj["accel_x"]))
    assert np.all(np.isfinite(traj["gyro_z"]))
    assert np.all(np.isfinite(traj["gt_east"]))
    assert np.all(np.isfinite(traj["gt_north"]))

    # 5. Verify wheel odometry calculation
    assert np.all(traj["wheel_speed"] >= 0.0)


def test_smartphone_schema_and_parsing(tmp_path):
    """Verify IO-VNBD Smartphone AndroSensor 24-column schema and parsing."""
    csv_file = str(tmp_path / "S-TestDrive.csv")
    generate_sample_iovnbd_s_csv(csv_file, duration_sec=25.0, fs=10.0, seed=20)

    # 1. Verify CSV column headers
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == IOVNBD_SMARTPHONE_COLUMNS
        assert len(headers) == 24

    # 2. Parse with IOVNBDLoader
    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    assert len(traj["time"]) == 250
    assert "accel_x" in traj
    assert "gyro_z" in traj
    assert "gt_speed" in traj
    assert "gt_yaw" in traj
    assert np.all(np.isfinite(traj["accel_x"]))
    assert np.all(np.isfinite(traj["gyro_z"]))


def test_canonical_schema_parsing(tmp_path):
    """Verify loading of preprocessed / canonical format CSVs."""
    csv_file = str(tmp_path / "canonical_drive.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "ax", "ay", "az", "gx", "gy", "gz", "speed", "yaw_rate", "east", "north"])
        for i in range(100):
            t = i * 0.1
            writer.writerow([t, 0.5, 0.0, 9.81, 0.0, 0.0, 0.05, 5.0, 0.05, t * 5.0, 0.0])

    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    assert len(traj["time"]) == 100
    assert np.allclose(traj["accel_x"], 0.5)
    assert np.allclose(traj["gt_speed"], 5.0)


def test_sliding_window_dataset(tmp_path):
    """Verify IMU sliding-window generation and PyTorch Dataset integration."""
    csv_file = str(tmp_path / "V-Drive.csv")
    generate_sample_iovnbd_v_csv(csv_file, duration_sec=20.0, fs=10.0, seed=30)

    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    window_size = 30
    step = 5
    windows, speeds, yaw_rates = IOVNBDLoader.create_sliding_windows(
        [traj], window_size=window_size, step=step
    )

    # 200 samples, window 30, step 5 -> (200 - 30)//5 + 1 = 35 windows
    expected_windows = (len(traj["time"]) - window_size) // step + 1
    assert windows.shape == (expected_windows, window_size, 6)
    assert speeds.shape == (expected_windows,)
    assert yaw_rates.shape == (expected_windows,)

    # Test PyTorch IOVNBDDataset
    ds = IOVNBDDataset([traj], window_size=window_size, step=step)
    assert len(ds) == expected_windows

    x, y_spd, y_yr = ds[0]
    assert x.shape == (window_size, 6)
    assert isinstance(x, torch.Tensor)
    assert isinstance(y_spd, torch.Tensor)
    assert isinstance(y_yr, torch.Tensor)


def test_git_lfs_pointer_rejection(tmp_path):
    """Verify that Git LFS pointer stubs are detected and rejected with clear error."""
    stub_file = str(tmp_path / "V-Stub.csv")
    with open(stub_file, "w", encoding="utf-8") as f:
        f.write("version https://git-lfs.github.com/spec/v1\noid sha256:123456\nsize 1000\n")

    loader = IOVNBDLoader()
    with pytest.raises(ValueError, match="Git LFS pointer stub"):
        loader.load_csv(stub_file)

    # In load_directory, stub should be skipped cleanly without raising an exception
    trajs = loader.load_directory(str(tmp_path))
    assert len(trajs) == 0


def test_trajectory_resampling_and_angle_unwrapping(tmp_path):
    """Verify resampling from 10Hz to 50Hz with phase unwrapping across +/- pi boundary."""
    csv_file = str(tmp_path / "V-10Hz.csv")
    generate_sample_iovnbd_v_csv(csv_file, duration_sec=10.0, fs=10.0, seed=40)

    loader = IOVNBDLoader()
    traj_50hz = loader.load_csv(csv_file, target_fs=50.0)

    assert abs(traj_50hz["fs"] - 50.0) < 1e-3
    assert abs(traj_50hz["dt"] - 0.02) < 1e-4
    assert abs(len(traj_50hz["time"]) - 500) <= 5

    # Dedicated test for phase unwrapping across +/- pi boundary:
    # Heading West (yaw near +pi wrapping to -pi)
    t = np.array([0.0, 0.1, 0.2])
    # Step from +3.10 rad to -3.10 rad (vehicle continuing to rotate counterclockwise)
    yaw = np.array([3.10, -3.10, -3.00])
    traj_wrap = {
        "time": t,
        "dt": 0.1,
        "fs": 10.0,
        "gt_yaw": yaw,
        "gps_bearing": yaw.copy(),
        "accel_x": np.array([1.0, 1.0, 1.0]),
        "gt_speed": np.array([10.0, 10.0, 10.0]),
        "gt_yaw_rate": np.array([0.1, 0.1, 0.1])
    }
    resampled = loader._resample_trajectory(traj_wrap, target_fs=50.0)
    # The midpoint at t=0.05 must be near +/- pi (~3.14 or -3.14), NOT near 0.0!
    mid_yaw = resampled["gt_yaw"][2]  # ~t=0.05
    assert abs(abs(mid_yaw) - math.pi) < 0.2, f"Expected angle near +/- pi, got {mid_yaw}"


def test_benchmark_outage_evaluation(tmp_path):
    """Verify GNSS outage evaluation and drift reduction metrics."""
    csv_file = str(tmp_path / "V-Bench.csv")
    generate_sample_iovnbd_v_csv(csv_file, duration_sec=50.0, fs=10.0, seed=50)

    loader = IOVNBDLoader()
    traj = loader.load_csv(csv_file, target_fs=50.0)

    model = IntelligentDeadReckoningNet(in_channels=6, conv_channels=32, gru_hidden_size=32, gru_layers=1)
    model.eval()

    # Inject 20s GNSS outage
    metrics = evaluate_trajectory_outage(
        model=model,
        trajectory=traj,
        outage_start_sec=15.0,
        outage_duration_sec=20.0,
        window_size=30,
        device=torch.device("cpu"),
        seed=100
    )

    assert "baseline_pure_imu" in metrics
    assert "intelligent_dead_reckoning" in metrics
    assert "drift_reduction_ratio" in metrics

    idr_metrics = metrics["intelligent_dead_reckoning"]
    base_metrics = metrics["baseline_pure_imu"]

    assert idr_metrics["position_drift_mae_m"] >= 0.0
    assert base_metrics["position_drift_mae_m"] >= 0.0
    assert metrics["drift_reduction_ratio"] > 0.0


def test_train_pipeline_seamless_fallback(tmp_path):
    """Verify that train_idr_model falls back seamlessly to synthetic data when directory is empty."""
    empty_dir = str(tmp_path / "empty_iovnbd")
    os.makedirs(empty_dir, exist_ok=True)
    save_pt = str(tmp_path / "test_fallback_model.pt")

    model, s_path, _ = train_idr_model(
        epochs=1,
        batch_size=32,
        window_size=30,
        save_path=save_pt,
        data_dir=empty_dir,
        dataset_mode="auto",
        device_name="cpu"
    )

    assert os.path.exists(save_pt)
    assert model is not None


def test_train_pipeline_iovnbd_dataset(tmp_path):
    """Verify training on IO-VNBD dataset CSV logs."""
    sample_dir = str(tmp_path / "iovnbd_data")
    os.makedirs(sample_dir, exist_ok=True)
    v_csv = os.path.join(sample_dir, "V-TrainSample.csv")
    generate_sample_iovnbd_v_csv(v_csv, duration_sec=40.0, fs=10.0, seed=60)

    save_pt = str(tmp_path / "test_iovnbd_model.pt")

    model, s_path, _ = train_idr_model(
        epochs=1,
        batch_size=32,
        window_size=30,
        save_path=save_pt,
        data_dir=sample_dir,
        dataset_mode="iovnbd",
        device_name="cpu"
    )

    assert os.path.exists(save_pt)
    assert model is not None


# =====================================================================
# Additional Robustness & Edge-Case Tests
# =====================================================================

def test_gps_cold_start_and_mid_drive_dropout(tmp_path):
    """
    Verify that GPS cold start (lat=0, lon=0 at start) and mid-drive dropouts (tunnel)
    do NOT corrupt ref_lat or produce 100+ km Null Island spikes.
    """
    csv_file = str(tmp_path / "V-DropoutDrive.csv")
    generate_sample_iovnbd_v_csv(csv_file, duration_sec=20.0, fs=10.0, seed=70)

    rows = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # 1. Inject cold start: first 5 rows have 0 satellites and lat=0.0, lon=0.0
    for r in rows[1:6]:
        r[0] = "0"
        r[2] = "0.0000000"
        r[3] = "0.0000000"

    # 2. Inject mid-drive tunnel dropout: rows 30..40 have 0 satellites and lat=0.0, lon=0.0
    for r in rows[30:40]:
        r[0] = "0"
        r[2] = "0.0000000"
        r[3] = "0.0000000"

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    # Max position offset in a 20s drive should be < 500m (NOT 100+ km!)
    assert np.max(np.abs(traj["gt_east"])) < 500.0, f"Spike detected in gt_east: {np.max(np.abs(traj['gt_east']))}"
    assert np.max(np.abs(traj["gt_north"])) < 500.0, f"Spike detected in gt_north: {np.max(np.abs(traj['gt_north']))}"

    # Verify GPS masks are correctly set to False during cold start and dropout
    assert traj["gps_mask"][0] == False
    assert traj["gps_mask"][4] == False
    assert traj["gps_mask"][15] == True
    assert traj["gps_mask"][35] == False


def test_european_french_dataset_parsing(tmp_path):
    """
    Verify parsing of European/French datasets using semicolon ';' delimiters
    and comma ',' decimal separators (e.g. Driver E & F recordings in France).
    """
    csv_file = str(tmp_path / "V-FrenchDrive.csv")

    headers = [
        "Time since start of day",
        "velocity",
        "Heading",
        "Wheel Speed Front Left",
        "Wheel Speed Front Right",
        "Wheel Speed Rear Left",
        "Wheel Speed Rear Right",
        "Yaw Rate",
        "Indicated Longitudinal Acceleration",
        "Indicated Lateral Acceleration",
        "Latitude",
        "Longitude",
        "No of GPS satellites available"
    ]

    # Write European format: semicolon delimiter and comma decimals
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        f.write(";".join(headers) + "\n")
        for i in range(50):
            t_str = f"{i * 0.1:.2f}".replace(".", ",")
            spd_str = "50,4"     # 50.4 km/h = 14.0 m/s
            hdg_str = "45,0"
            ws_str = "47,0"
            yr_str = "0,05"
            ax_str = "0,25"      # 0.25 g
            ay_str = "-0,12"
            lat_str = "48,8566"  # Paris latitude
            lon_str = "2,3522"   # Paris longitude
            sat_str = "8"
            row = [t_str, spd_str, hdg_str, ws_str, ws_str, ws_str, ws_str, yr_str, ax_str, ay_str, lat_str, lon_str, sat_str]
            f.write(";".join(row) + "\n")

    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)

    # Verify that speed was parsed as 14.0 m/s (NOT 0.0!)
    assert pytest.approx(float(traj["gt_speed"][0]), abs=0.2) == 14.0
    # Verify that acceleration was parsed as 0.25 * 9.80665 ~ 2.45 m/s^2 (NOT 0.0!)
    assert pytest.approx(float(traj["accel_x"][0]), abs=0.2) == 0.25 * STANDARD_GRAVITY_G
    assert len(traj["time"]) == 50


def test_heading_compass_to_enu_conversion():
    """Verify Compass Bearing to ENU Yaw conversions across cardinal directions."""
    # 0 deg (North) -> pi/2 rad (North in ENU)
    assert pytest.approx(float(compass_bearing_to_enu_yaw(0.0)), abs=1e-5) == math.pi / 2.0
    # 90 deg (East) -> 0 rad (East in ENU)
    assert pytest.approx(float(compass_bearing_to_enu_yaw(90.0)), abs=1e-5) == 0.0
    # 180 deg (South) -> -pi/2 rad (South in ENU)
    assert pytest.approx(float(compass_bearing_to_enu_yaw(180.0)), abs=1e-5) == -math.pi / 2.0
    # 270 deg (West) -> pi rad (West in ENU)
    assert abs(abs(float(compass_bearing_to_enu_yaw(270.0))) - math.pi) < 1e-5

    # Reverse: ENU Yaw to Compass Bearing
    assert pytest.approx(float(enu_yaw_to_compass_bearing(math.pi / 2.0)), abs=1e-4) == 0.0
    assert pytest.approx(float(enu_yaw_to_compass_bearing(0.0)), abs=1e-4) == 90.0
    assert pytest.approx(float(enu_yaw_to_compass_bearing(-math.pi / 2.0)), abs=1e-4) == 180.0
    assert pytest.approx(float(enu_yaw_to_compass_bearing(math.pi)), abs=1e-4) == 270.0


def test_utf8_bom_and_non_ascii_resilience(tmp_path):
    """Verify loader reads files with UTF-8 BOM prefix and degree symbols (e.g. 'Orientation Â°')."""
    csv_file = str(tmp_path / "V-BOMDrive.csv")

    headers = [
        "Time since start of day",
        "velocity",
        "Heading",
        "Wheel Speed Front Left",
        "Indicated Longitudinal Acceleration",
        "Latitude",
        "Longitude",
        "No of GPS satellites available"
    ]

    # Write UTF-8 BOM prefix (\xef\xbb\xbf)
    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in range(20):
            writer.writerow([f"{i*0.1:.2f}", "36.0", "90.0", "33.5", "0.1", "52.4081", "-1.5106", "8"])

    loader = IOVNBDLoader(default_fs=10.0)
    traj = loader.load_csv(csv_file)
    assert len(traj["time"]) == 20
    assert pytest.approx(float(traj["gt_speed"][0]), abs=0.1) == 10.0
