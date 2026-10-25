from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class IMUPacket(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds or epoch")
    accel_x: float = Field(..., description="Forward / lateral acceleration X in m/s^2")
    accel_y: float = Field(..., description="Lateral / forward acceleration Y in m/s^2")
    accel_z: float = Field(..., description="Vertical acceleration Z in m/s^2")
    gyro_x: float = Field(..., description="Angular rate X in rad/s")
    gyro_y: float = Field(..., description="Angular rate Y in rad/s")
    gyro_z: float = Field(..., description="Yaw angular rate Z in rad/s")

class GNSSPacket(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds")
    latitude: float = Field(..., description="WGS84 Latitude in degrees")
    longitude: float = Field(..., description="WGS84 Longitude in degrees")
    altitude: Optional[float] = Field(0.0, description="Altitude in meters")
    speed_ms: Optional[float] = Field(None, description="Ground speed in m/s")
    bearing_deg: Optional[float] = Field(None, description="Course over ground in degrees")
    accuracy_m: Optional[float] = Field(3.0, description="Estimated accuracy in meters")

class TelemetryFeedRequest(BaseModel):
    imu: IMUPacket
    gnss: Optional[GNSSPacket] = None
    simulate_outage: bool = False

class SimulationStartRequest(BaseModel):
    duration_sec: float = 120.0
    outage_start_sec: float = 40.0
    outage_end_sec: float = 85.0
    playback_speed: float = 1.0

class OutageToggleRequest(BaseModel):
    outage_active: bool
