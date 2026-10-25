import os
import pytest
from models.online_calibrator import OnlineDriftCalibrator

def test_online_drift_learning():
    tmp_path = "test_device_profile.json"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    calib = OnlineDriftCalibrator(profile_path=tmp_path)
    
    # Simulate a scenario where raw model predicts 10.0 m/s, but GPS ground truth is consistently 11.0 m/s
    # (e.g. 10% tire circumference variation or device mounting scale factor)
    for _ in range(50):
        calib.calibrate_step(
            predicted_vel=10.0,
            predicted_yaw_rate=0.0,
            gps_speed=11.0,
            gps_bearing_rate=0.0,
            gps_accuracy_m=1.5,
            is_stationary=False
        )

    # Scale factor or bias should have adapted upward
    calib_v, _ = calib.apply_correction(10.0, 0.0)
    assert calib_v > 10.2  # Adapted towards 11.0 m/s

    # Test ZUPT recalibration
    calib.calibrate_step(
        predicted_vel=0.5,
        predicted_yaw_rate=0.02,
        gps_speed=0.0,
        gps_bearing_rate=0.0,
        is_stationary=True
    )
    assert calib.zupt_counter > 0

    # Save and reload
    calib.save_profile()
    assert os.path.exists(tmp_path)

    reloaded = OnlineDriftCalibrator(profile_path=tmp_path)
    assert reloaded.samples_learned == calib.samples_learned
    assert pytest.approx(reloaded.scale_v) == calib.scale_v

    # Cleanup
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

def test_degraded_gps_rejection():
    tmp_path = "test_degraded_profile.json"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    calib = OnlineDriftCalibrator(profile_path=tmp_path)
    res = calib.calibrate_step(
        predicted_vel=10.0,
        predicted_yaw_rate=0.0,
        gps_speed=15.0,
        gps_bearing_rate=0.0,
        gps_accuracy_m=8.0,  # poor accuracy (e.g. multipath reflection)
        is_stationary=False
    )
    assert res["adapted"] is False
    assert res["reason"] == "gps_unavailable_or_degraded"
    assert calib.samples_learned == 0

    if os.path.exists(tmp_path):
        os.remove(tmp_path)
