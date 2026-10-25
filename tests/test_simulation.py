import numpy as np
import pytest
from simulation.dataset_generator import VehicularTrajectoryGenerator

def test_vehicular_trajectory_generation():
    gen = VehicularTrajectoryGenerator(sampling_rate_hz=50.0, seed=123)
    data = gen.generate_synthetic_drive(duration_sec=30.0, outage_windows=[(10.0, 20.0)])

    assert "accel_x" in data
    assert "gyro_z" in data
    assert "gt_speed" in data
    assert "gps_mask" in data
    assert len(data["time"]) == 30 * 50

    # Verify outage mask
    t = data["time"]
    gps_mask = data["gps_mask"]

    # During 10s to 20s, no GPS points should be valid
    outage_indices = np.where((t >= 10.0) & (t <= 20.0))[0]
    assert np.all(~gps_mask[outage_indices])

    # Outside outage, there should be valid GPS readings at 1Hz
    pre_outage_indices = np.where(t < 10.0)[0]
    assert np.any(gps_mask[pre_outage_indices])
