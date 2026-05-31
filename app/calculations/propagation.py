"""
Модель дождя для расчета затухания сигнала в спутниковой связи.
из чата гпт для теста потом улучшить (сделать для определенного спутника)

"""
import math
from ..validation.validators import validate_positive_finite, validate_range, validate_non_negative

# ITU-R P.838 коэффициенты для горизонтальной поляризации
# (frequency_ghz → (k, alpha))
ITU_RAIN_COEFFICIENTS: dict[float, tuple[float, float]] = {
    1.0:  (0.0000387, 0.912),
    2.0:  (0.000154,  0.963),
    4.0:  (0.000650,  1.121),
    6.0:  (0.00175,   1.308),
    7.0:  (0.00301,   1.332),
    8.0:  (0.00454,   1.327),
    10.0: (0.0101,    1.276),
    12.0: (0.0188,    1.217),
    15.0: (0.0367,    1.154),
    20.0: (0.0751,    1.099),
    25.0: (0.124,     1.061),
    30.0: (0.187,     1.021),
    40.0: (0.350,     0.939),
    50.0: (0.536,     0.873),
}

# ITU-R P.837 — интенсивность дождя (мм/ч) для 0.01% времени по климатическим зонам
RAIN_RATE_MM_H: dict[str, float] = {
    "A": 8,   "B": 12,  "C": 15,  "D": 19,
    "E": 22,  "F": 28,  "G": 30,  "H": 32,
    "J": 35,  "K": 42,  "L": 60,  "M": 63,
    "N": 95,  "P": 145, "Q": 115,
}


def _get_itu_coefficients(frequency_ghz: float) -> tuple[float, float]:
    """Interpolate ITU-R P.838 k and alpha for given frequency."""
    freqs = sorted(ITU_RAIN_COEFFICIENTS.keys())

    if frequency_ghz <= freqs[0]:
        return ITU_RAIN_COEFFICIENTS[freqs[0]]
    if frequency_ghz >= freqs[-1]:
        return ITU_RAIN_COEFFICIENTS[freqs[-1]]

    # Линейная интерполяция
    for i in range(len(freqs) - 1):
        f1, f2 = freqs[i], freqs[i + 1]
        if f1 <= frequency_ghz <= f2:
            t = (frequency_ghz - f1) / (f2 - f1)
            k1, a1 = ITU_RAIN_COEFFICIENTS[f1]
            k2, a2 = ITU_RAIN_COEFFICIENTS[f2]
            return k1 + t * (k2 - k1), a1 + t * (a2 - a1)

    return ITU_RAIN_COEFFICIENTS[freqs[-1]]


def calculate_atmospheric_loss(
    frequency_ghz: float,
    elevation_deg: float,
) -> float:
    """
    Calculate atmospheric gaseous attenuation (ITU-R P.676 simplified).

    Valid for elevation angles > 5 degrees.
    Accounts for oxygen (~0.035 dB/km) and water vapour (~0.035 dB/km).

    Args:
        frequency_ghz: Carrier frequency in GHz. Must be > 0.
        elevation_deg: Elevation angle in degrees. Must be 5–90.

    Returns:
        Atmospheric attenuation in dB.
    """
    validate_positive_finite(frequency_ghz=frequency_ghz)
    validate_range(elevation_deg, 5.0, 90.0, "elevation_deg")

    elevation_rad = math.radians(elevation_deg)

    # Зенитное затухание: кислород + водяной пар (типовые значения)
    zenith_oxygen_db = 0.035
    zenith_water_vapour_db = 0.035

    # Пересчёт через угол места
    return (zenith_oxygen_db + zenith_water_vapour_db) / math.sin(elevation_rad)


def calculate_rain_loss(
    frequency_ghz: float,
    elevation_deg: float,
    climate_zone: str,
    altitude_m: float = 0.0,
    availability_pct: float = 99.9,
) -> float:
    """
    Calculate rain attenuation (ITU-R P.618).

    Args:
        frequency_ghz: Carrier frequency in GHz. Must be > 0.
        elevation_deg: Elevation angle in degrees. Must be 5–90.
        climate_zone: ITU rain climate zone (A–Q).
        altitude_m: Earth station altitude above sea level in meters.
        availability_pct: Required link availability in %. Default 99.9.

    Returns:
        Rain attenuation in dB for given availability.

    Raises:
        ValueError: If climate_zone is unknown or parameters are invalid.
    """
    validate_positive_finite(frequency_ghz=frequency_ghz)
    validate_range(elevation_deg, 5.0, 90.0, "elevation_deg")
    validate_non_negative(altitude_m=altitude_m)
    validate_range(availability_pct, 90.0, 99.999, "availability_pct")

    if climate_zone not in RAIN_RATE_MM_H:
        raise ValueError(
            f"Unknown climate zone: '{climate_zone}'. "
            f"Available zones: {list(RAIN_RATE_MM_H.keys())}"
        )

    rain_rate = RAIN_RATE_MM_H[climate_zone]
    elevation_rad = math.radians(elevation_deg)

    # ITU-R P.618 Step 1: высота дождя (км)
    rain_height_km = 5.0 - 0.075 * (abs(0) - 23)  # упрощённо для средних широт

    # Step 2: наклонная длина пути через дождь
    if elevation_deg >= 5:
        slant_path_km = (rain_height_km - altitude_m / 1000) / math.sin(elevation_rad)
    else:
        slant_path_km = 2 * (rain_height_km - altitude_m / 1000) / (
            math.sin(2 * elevation_rad) + (2 * (rain_height_km - altitude_m / 1000) / 8160)
        )

    slant_path_km = max(slant_path_km, 0.0)

    # Step 3: горизонтальная проекция
    horizontal_path_km = slant_path_km * math.cos(elevation_rad)

    # Step 4: специфическое затухание γ_R = k * R^alpha
    k, alpha = _get_itu_coefficients(frequency_ghz)
    gamma_r = k * (rain_rate ** alpha)

    # Step 5: коэффициент сокращения пути
    r_factor = 1 / (1 + horizontal_path_km / 35 * math.exp(-0.015 * rain_rate))

    # Step 6: эффективная длина пути
    effective_path_km = horizontal_path_km * r_factor

    # Step 7: затухание для 0.01% времени
    rain_loss_001 = gamma_r * effective_path_km

    # Step 8: пересчёт на нужную доступность (ITU-R P.618 формула масштабирования)
    unavailability_pct = 100 - availability_pct
    if unavailability_pct <= 0.01:
        return rain_loss_001

    # Scaling formula ITU-R P.618
    beta = (
        -0.00022 * abs(0) + 0.05
        if rain_loss_001 < 10
        else 0
    )
    scaling = (
        0.12 * (unavailability_pct / 0.01) ** (-(0.546 + 0.043 * math.log10(unavailability_pct / 0.01)))
    )
    return rain_loss_001 * scaling

# --- ИСПРАВЛЕННЫЙ БЛОК ВНУТРИ calculate_rain_loss ---
# def calculate_rain_loss_v2(
#     frequency_ghz: float,
#     elevation_deg: float,
#     latitude_deg: float,  # Добавили широту
#     climate_zone: str,
#     altitude_m: float = 0.0,
#     availability_pct: float = 99.9,
# ) -> float:
#     # ... (валидация как в вашем коде) ...
    
#     rain_rate = RAIN_RATE_MM_H[climate_zone]
#     elevation_rad = math.radians(elevation_deg)

#     # Шаг 1: Реальная высота дождя по ITU-R P.618 для широты станции
#     # hR зависит от широты (phi)
#     if latitude_deg < 36:
#         rain_height_km = 5.0
#     else:
#         rain_height_km = 5.0 - 0.075 * (latitude_deg - 36)

#     # ... (остальной код расчета slant_path и т.д. остается прежним) ...
#     # Не забудьте заменить abs(0) в расчете beta на latitude_deg
#     # beta = -0.00022 * latitude_deg + 0.05 ...
    
#     # [Здесь идет ваш алгоритм из шагов 2-8]
#     # ...
#     return rain_loss_final