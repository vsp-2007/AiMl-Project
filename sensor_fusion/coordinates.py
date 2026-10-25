import math
import numpy as np

# WGS84 Ellipsoid constants
WGS84_A = 6378137.0          # Semi-major axis in meters
WGS84_E_SQ = 0.00669437999014  # First eccentricity squared

class CoordinateTransformer:
    """
    Transforms coordinates between Geodetic (Lat, Lon, Alt in WGS84)
    and Local Tangent Plane (ENU: East, North, Up in meters).
    Essential for Dead Reckoning and Kalman Filtering in metric space.
    """
    def __init__(self, ref_lat_deg: float, ref_lon_deg: float, ref_alt_m: float = 0.0):
        self.ref_lat_deg = ref_lat_deg
        self.ref_lon_deg = ref_lon_deg
        self.ref_alt_m = ref_alt_m
        
        self.ref_lat_rad = math.radians(ref_lat_deg)
        self.ref_lon_rad = math.radians(ref_lon_deg)
        
        self.ref_ecef_x, self.ref_ecef_y, self.ref_ecef_z = self.geodetic_to_ecef(
            ref_lat_deg, ref_lon_deg, ref_alt_m
        )

    @staticmethod
    def geodetic_to_ecef(lat_deg: float, lon_deg: float, alt_m: float = 0.0):
        lat = math.radians(lat_deg)
        lon = math.radians(lon_deg)
        sin_lat = math.sin(lat)
        cos_lat = math.cos(lat)
        sin_lon = math.sin(lon)
        cos_lon = math.cos(lon)

        n = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat * sin_lat)
        x = (n + alt_m) * cos_lat * cos_lon
        y = (n + alt_m) * cos_lat * sin_lon
        z = (n * (1.0 - WGS84_E_SQ) + alt_m) * sin_lat
        return x, y, z

    def geodetic_to_enu(self, lat_deg: float, lon_deg: float, alt_m: float = 0.0):
        x, y, z = self.geodetic_to_ecef(lat_deg, lon_deg, alt_m)
        dx = x - self.ref_ecef_x
        dy = y - self.ref_ecef_y
        dz = z - self.ref_ecef_z

        sin_lat = math.sin(self.ref_lat_rad)
        cos_lat = math.cos(self.ref_lat_rad)
        sin_lon = math.sin(self.ref_lon_rad)
        cos_lon = math.cos(self.ref_lon_rad)

        east = -sin_lon * dx + cos_lon * dy
        north = -sin_lat * cos_lon * dx - sin_lat * sin_lon * dy + cos_lat * dz
        up = cos_lat * cos_lon * dx + cos_lat * sin_lon * dy + sin_lat * dz
        return east, north, up

    def enu_to_geodetic(self, east: float, north: float, up: float = 0.0):
        sin_lat = math.sin(self.ref_lat_rad)
        cos_lat = math.cos(self.ref_lat_rad)
        sin_lon = math.sin(self.ref_lon_rad)
        cos_lon = math.cos(self.ref_lon_rad)

        # Inverse rotation from ENU to ECEF delta
        dx = -sin_lon * east - sin_lat * cos_lon * north + cos_lat * cos_lon * up
        dy = cos_lon * east - sin_lat * sin_lon * north + cos_lat * sin_lon * up
        dz = cos_lat * north + sin_lat * up

        x = self.ref_ecef_x + dx
        y = self.ref_ecef_y + dy
        z = self.ref_ecef_z + dz

        # ECEF to Geodetic (Bowring's algorithm with polar numerical stabilization)
        b = WGS84_A * math.sqrt(1.0 - WGS84_E_SQ)
        p = math.sqrt(x * x + y * y)
        if p < 1e-6:
            lat_deg = 90.0 if z > 0 else -90.0
            alt = abs(z) - b
            return lat_deg, self.ref_lon_deg, alt

        theta = math.atan2(z * WGS84_A, p * b)
        e_prime_sq = WGS84_E_SQ / (1.0 - WGS84_E_SQ)

        lat = math.atan2(
            z + e_prime_sq * b * (math.sin(theta) ** 3),
            p - WGS84_E_SQ * WGS84_A * (math.cos(theta) ** 3)
        )
        lon = math.atan2(y, x)

        sin_lat_res = math.sin(lat)
        cos_lat_res = math.cos(lat)
        n = WGS84_A / math.sqrt(1.0 - WGS84_E_SQ * sin_lat_res * sin_lat_res)
        
        # Avoid division by cos(lat) near poles (lat > 45 deg)
        if abs(sin_lat_res) > 0.7071:
            alt = (abs(z) / abs(sin_lat_res)) - n * (1.0 - WGS84_E_SQ)
        else:
            alt = (p / cos_lat_res) - n

        return math.degrees(lat), math.degrees(lon), alt
