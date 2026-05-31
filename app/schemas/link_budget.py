from pydantic import BaseModel, Field
from enum import Enum

class ModulationType(str, Enum):
    BPSK = "BPSK"
    QPSK = "QPSK"
    PSK8 = "8PSK"
    APSK16 = "16APSK"
    APSK32 = "32APSK"

class FecRate(str, Enum):
    """FEC коды для DVB-S2 (базовый набор)"""
    R_1_2 = "1/2"
    R_2_3 = "2/3"
    R_3_4 = "3/4"
    R_4_5 = "4/5"
    R_5_6 = "5/6"
    R_7_8 = "7/8"

class ClimateZone(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    P = "P"
    Q = "Q"

class TransmitSide(BaseModel):
    tx_power_w: float = Field(..., gt=0, description="TX power in Watts")
    tx_losses_db: float = Field(0.0, ge=0, description="Feedline losses in dB")
    antenna_diameter_m: float = Field(..., gt=0, description="Antenna diameter in meters")
    antenna_efficiency: float = Field(0.65, gt=0, le=1.0, description="Antenna efficiency 0-1")

class ReceiveSide(BaseModel):
    antenna_diameter_m: float = Field(..., gt=0, description="Antenna diameter in meters")
    antenna_efficiency: float = Field(0.65, gt=0, le=1.0, description="Antenna efficiency 0-1")
    noise_figure_db: float = Field(..., gt=0, description="LNB noise figure in dB")
    line_loss_db: float = Field(0.0, ge=0, description="Feedline loss antenna→receiver")
    antenna_noise_temp_k: float = Field(35.0, gt=0, description="Antenna noise temperature in K")

class GroundStationParams(BaseModel):
    latitude_deg: float = Field(..., ge=-90, le=90, description="Ground station latitude in degrees")
    longitude_deg: float = Field(..., ge=-180, le=180, description="Ground station longitude in degrees")
    altitude_m: float = Field(0.0, ge=0, description="Ground station altitude in meters")

class SatellitePositionParams(BaseModel):
    longitude_deg: float = Field(..., ge=-180, le=180, description="Satellite longitude in degrees" )
    altitude_km: float = Field(35786.0, gt=0, description="Satellite altitude in kilometers")

class PropagationParams(BaseModel):
    ground_station: GroundStationParams
    satellite_position: SatellitePositionParams
    availability_pct: float = Field(99.9, gt=0, le=100, description="Link availability percentage")
    climate_zone: ClimateZone = Field(ClimateZone.K, description="Climate zone for rain attenuation")   
    elevation_deg: float = Field(None, ge=0, le=360, description="Elevation in deg")
    slant_range_km: float = Field(None, gt=0, description="Slant range in km (calculated or entered manually)")

class LinkParams(BaseModel):
    frequency_ghz: float = Field(..., gt=0, description="Carrier frequency in GHz")
    bandwidth_hz: float = Field(..., gt=0, description="Signal bandwidth in Hz")
    modulation: ModulationType = Field(..., description="Modulation")
    fec_rate: FecRate = Field(..., description="FEC code rate")
    implementation_magin_db: float = Field(1.0, gt=0, description="Implementation margin in dB")
    roll_off_factor: float = Field(0.20, gt=0.05, le=0.35, description="Roll-off factor")

class LinkBudgetRequest(BaseModel):
    transmit_side: TransmitSide
    receive_side: ReceiveSide
    propagation: PropagationParams
    link_params: LinkParams

class TransmitResult(BaseModel):
    tx_power_dbw: float
    antenna_gain_dbi: float
    eirp_dbw: float

class PathResult(BaseModel):
    fspl_db: float
    atmospheric_loss_db: float
    rain_loss_db: float
    total_path_loss_db: float

class ReceiveResult(BaseModel):
    antenna_gain_dbi: float
    receive_noise_temp_k: float
    system_noise_temp_k: float
    g_over_t_db_k: float

class PerformanceResult(BaseModel):
    cn_db: float
    cn0_db_hz: float
    eb_n0_db: float
    required_eb_n0_db: float
    implementation_margin_db: float
    link_margin_db: float
    is_viable: bool # link_margin > 0

class GeometryResult(BaseModel):
    elevation_deg: float
    slant_range_km: float

class LinkBudgetResponse(BaseModel):
    transmit: TransmitResult
    path: PathResult
    receive: ReceiveResult
    performance: PerformanceResult
    geometry: GeometryResult



