import math
import pytest
from sensor_fusion.coordinates import CoordinateTransformer

def test_coordinate_roundtrip():
    ref_lat = 12.9716
    ref_lon = 77.5946
    ref_alt = 920.0
    transformer = CoordinateTransformer(ref_lat, ref_lon, ref_alt)

    # Test point ~ 500m East, 300m North, 10m Up
    test_east = 500.0
    test_north = 300.0
    test_up = 10.0

    lat, lon, alt = transformer.enu_to_geodetic(test_east, test_north, test_up)
    calc_east, calc_north, calc_up = transformer.geodetic_to_enu(lat, lon, alt)

    assert pytest.approx(calc_east, abs=1e-3) == test_east
    assert pytest.approx(calc_north, abs=1e-3) == test_north
    assert pytest.approx(calc_up, abs=1e-2) == test_up

def test_zero_offset():
    transformer = CoordinateTransformer(13.0827, 80.2707, 10.0)
    e, n, u = transformer.geodetic_to_enu(13.0827, 80.2707, 10.0)
    assert abs(e) < 1e-4
    assert abs(n) < 1e-4
    assert abs(u) < 1e-4

def test_polar_and_high_latitude():
    # Test near North pole (e.g. 89.5 deg latitude)
    transformer = CoordinateTransformer(89.5, 0.0, 50.0)
    lat, lon, alt = transformer.enu_to_geodetic(0.0, 0.0, 0.0)
    assert pytest.approx(lat, abs=1e-5) == 89.5
    assert pytest.approx(alt, abs=1e-2) == 50.0

    # Test exact North Pole
    pole_transformer = CoordinateTransformer(90.0, 0.0, 0.0)
    lat, lon, alt = pole_transformer.enu_to_geodetic(0.0, 0.0, 0.0)
    assert pytest.approx(lat, abs=1e-5) == 90.0
    assert abs(alt) < 0.1
