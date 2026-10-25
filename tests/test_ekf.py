import math
import numpy as np
import pytest
from sensor_fusion.ekf import IntelligentEKF, normalize_angle

def test_angle_normalization():
    assert pytest.approx(normalize_angle(0.0)) == 0.0
    assert pytest.approx(normalize_angle(math.pi)) == math.pi
    assert pytest.approx(normalize_angle(3 * math.pi)) == math.pi
    assert pytest.approx(normalize_angle(-3 * math.pi)) == -math.pi

def test_ekf_prediction_and_gnss_update():
    ekf = IntelligentEKF(init_east=0.0, init_north=0.0, init_velocity=10.0, init_yaw_rad=0.0)
    
    # Predict 1 second of forward driving (East direction: yaw=0)
    dt = 0.1
    for _ in range(10):
        ekf.predict(dt=dt, accel_fwd=0.0, gyro_yaw_rate=0.0)
    
    state = ekf.get_state()
    # After 1s at 10m/s, East should be ~10m
    assert pytest.approx(state["east_m"], abs=0.5) == 10.0
    assert pytest.approx(state["north_m"], abs=0.5) == 0.0

    # GNSS Measurement update at (10.5, 0.2)
    res = ekf.update_gnss(east=10.5, north=0.2, speed=10.2, bearing_rad=0.0)
    updated_state = ekf.get_state()
    assert abs(updated_state["east_m"] - 10.5) < 1.0
    assert abs(updated_state["north_m"] - 0.2) < 1.0
    assert updated_state["outage_active"] is False

def test_ekf_outage_and_ml_update():
    ekf = IntelligentEKF(init_east=100.0, init_north=50.0, init_velocity=15.0, init_yaw_rad=0.0)
    
    # Enter outage
    ekf.mark_outage(0.02)
    assert ekf.outage_active is True
    assert ekf.outage_duration_s > 0

    # ML update with predicted speed and yaw rate
    res = ekf.update_ml_prediction(
        predicted_velocity=14.8,
        predicted_yaw_rate=0.05,
        var_velocity=0.1,
        var_yaw_rate=0.001,
        dt=0.02,
        measured_gyro_yaw_rate=0.05
    )
    assert res["status"] == "ml_updated"
    state = ekf.get_state()
    assert abs(state["velocity_ms"] - 14.8) < 0.2

def test_ekf_no_double_yaw_integration():
    """Verify that yaw rate is not integrated twice during outage updates."""
    ekf = IntelligentEKF(init_east=0.0, init_north=0.0, init_velocity=10.0, init_yaw_rad=0.0)
    dt = 0.05
    turn_rate = 0.10  # 0.10 rad/s turn
    
    for _ in range(20):  # 1.0 second total (20 * 0.05s)
        ekf.predict(dt=dt, accel_fwd=0.0, gyro_yaw_rate=turn_rate)
        ekf.update_ml_prediction(
            predicted_velocity=10.0,
            predicted_yaw_rate=turn_rate,
            var_velocity=0.1,
            var_yaw_rate=0.001,
            dt=dt,
            measured_gyro_yaw_rate=turn_rate
        )
    
    state = ekf.get_state()
    # In 1 second at 0.10 rad/s, total heading change should be ~0.10 radians (NOT doubled to ~0.20)
    assert pytest.approx(state["yaw_rad"], abs=0.02) == 0.10

def test_ekf_zupt():
    ekf = IntelligentEKF(init_east=0.0, init_north=0.0, init_velocity=5.0, init_yaw_rad=0.0)
    # Perform ZUPT with a known constant gyro reading (e.g. 0.03 rad/s sensor drift while stopped)
    for _ in range(5):
        ekf.update_zupt(measured_yaw_rate=0.03)

    state = ekf.get_state()
    # Velocity should snap close to 0
    assert abs(state["velocity_ms"]) < 0.1
    # Yaw bias should track the 0.03 rad/s drift
    assert abs(state["yaw_bias_rads"] - 0.03) < 0.015
