import math
from ..calculations.antenna import calculate_antenna_gain
from ..calculations.eirp import calculate_eirp
from ..calculations.fspl import calculate_fspl
from ..calculations.noise import (
    calculate_receiver_noise_temperature,
    calculate_system_noise_temperature,
)
from ..calculations.gt import calculate_g_over_t
from ..calculations.cn import calculate_cn
from ..calculations.power import calculate_watts_to_dbw
from ..calculations.modulation import (
    get_required_eb_n0_db,
    calculate_bit_rate_bps,
    calculate_link_margin_db,
    calculate_eb_n0,
)
from ..calculations.propagation import (
    calculate_atmospheric_loss,
    calculate_rain_loss,
)
from ..schemas.link_budget import (
    LinkBudgetRequest,
    LinkBudgetResponse,
    GeometryResult,
    TransmitResult,
    PathResult,
    ReceiveResult,
    PerformanceResult,
)
from app.calculations.constants import LIGHT_SPEED
from app.calculations.geometry import calculate_link_geometry

def calculate_link_budget(request: LinkBudgetRequest) -> LinkBudgetResponse:
    # --- БЛОК 0: Геометрия ---
    prop = request.propagation
    gs = prop.ground_station
    sat = prop.satellite_position

    if prop.elevation_deg is None or prop.slant_range_km is None:
        geo = calculate_link_geometry(
            station_lat_deg=gs.latitude_deg,
            station_lon_deg=gs.longitude_deg,
            satellite_lon_deg=sat.longitude_deg,
            satellite_alt_km=sat.altitude_km,
        )
        elevation_deg = geo.elevation_deg
        slant_range_km = geo.slant_range_km
        propagation_delay_ms = geo.propagation_delay_ms
    else:
        # Если параметры введены вручную, используем их
        elevation_deg = prop.elevation_deg
        slant_range_km = prop.slant_range_km
        # Рассчитываем задержку на основе ручного ввода дистанции
        propagation_delay_ms = (slant_range_km / LIGHT_SPEED) * 1000

    # Проверка видимости спутника (горизонт)
    if elevation_deg <= 0:
        raise ValueError(
            f"Satellite is below the horizon for this location "
            f"(elevation = {elevation_deg:.2f}°). "
            f"Check ground station coordinates and satellite position."
        )
    
    # --- БЛОК 1: Передатчик ---
    tx_power_dbw = calculate_watts_to_dbw(request.transmit_side.tx_power_w)
    tx_gain_dbi = calculate_antenna_gain(
        request.transmit_side.antenna_diameter_m,
        request.link_params.frequency_ghz,
        request.transmit_side.antenna_efficiency,
    )
    eirp = calculate_eirp(
        tx_power_dbw=tx_power_dbw,
        antenna_gain_dbi=tx_gain_dbi,
        losses_db=request.transmit_side.tx_losses_db,
    )

    # --- БЛОК 2: Распространение ---
    fspl = calculate_fspl(
        frequency_ghz = request.link_params.frequency_ghz,
        distance_km = slant_range_km,
    )
    atm_loss = calculate_atmospheric_loss(
        frequency_ghz=request.link_params.frequency_ghz,
        elevation_deg=elevation_deg,
    )
    rain_loss = calculate_rain_loss(
        frequency_ghz=request.link_params.frequency_ghz,
        elevation_deg=elevation_deg,
        climate_zone=request.propagation.climate_zone.value,
        altitude_m=gs.altitude_m,
        availability_pct=request.propagation.availability_pct,
    )
    total_path_loss = fspl + atm_loss + rain_loss

    # --- БЛОК 3: Приёмник ---
    rx_gain = calculate_antenna_gain(
        request.receive_side.antenna_diameter_m,
        request.link_params.frequency_ghz,
        request.receive_side.antenna_efficiency,
    )
    rx_noise_tmp = calculate_receiver_noise_temperature(request.receive_side.noise_figure_db)
    sys_noise_temp = calculate_system_noise_temperature(
        request.receive_side.antenna_noise_temp_k,
        rx_noise_tmp,
        request.receive_side.line_loss_db,
    )
    g_over_t = calculate_g_over_t(antenna_gain_dbi=rx_gain, system_noise_temp_k=sys_noise_temp)

    # --- БЛОК 4: Качество ---
    bandwidth_hz = request.link_params.bandwidth_hz
    bandwidth_db = 10 * math.log10(bandwidth_hz)
    
    cn = calculate_cn(
        eirp_dbw=eirp,
        fspl_db=total_path_loss,
        g_over_t_db_k=g_over_t,
        bandwidth_hz=bandwidth_hz,
    )
    cn0 = cn + bandwidth_db 

    bit_rate_bps = calculate_bit_rate_bps(
        bandwidth_hz=bandwidth_hz,
        modulation=request.link_params.modulation,
        fec_rate=request.link_params.fec_rate.value,
        roll_off_factor=request.link_params.roll_off_factor,
    )

    eb_n0 = calculate_eb_n0(
        cn0_dbhz=cn0,
        bit_rate_bps=bit_rate_bps,
    )
    required_eb_n0 = get_required_eb_n0_db(
        modulation=request.link_params.modulation.value,
        fec_rate=request.link_params.fec_rate.value
    )
    margin = calculate_link_margin_db(
        eb_n0_db=eb_n0,
        required_eb_n0_db=required_eb_n0,
        implementation_margin_db=request.link_params.implementation_magin_db
    )

    return LinkBudgetResponse(
        geometry=GeometryResult(
            elevation_deg=elevation_deg,
            slant_range_km=round(slant_range_km, 1)
        ),
        transmit=TransmitResult(
            tx_power_dbw=round(tx_power_dbw, 2),
            antenna_gain_dbi=round(tx_gain_dbi, 2),
            eirp_dbw=round(eirp, 2),
        ),
        path=PathResult(
            fspl_db=round(fspl, 2),
            atmospheric_loss_db=round(atm_loss, 2),
            rain_loss_db=round(rain_loss, 2),
            total_path_loss_db=round(total_path_loss, 2)
        ),
        receive=ReceiveResult(
            antenna_gain_dbi=round(rx_gain, 2),
            receive_noise_temp_k=round(rx_noise_tmp, 2),
            system_noise_temp_k=round(sys_noise_temp, 2),
            g_over_t_db_k=round(g_over_t, 2),
        ),
        performance=PerformanceResult(
            cn_db=round(cn, 2),
            cn0_db_hz=round(cn0, 2),
            eb_n0_db=round(eb_n0, 2),
            required_eb_n0_db=round(required_eb_n0, 2),
            implementation_margin_db=request.link_params.implementation_magin_db,
            link_margin_db=round(margin, 2),
            is_viable=margin > 0,
        )
    )
