import math
from ..validation.validators import validate_finite, validate_positive_finite


def calculate_g_over_t(
        antenna_gain_dbi: float,
        system_noise_temp_k: float
) -> float:
    """
    Calculate G/T — Figure of Merit of receiving system.

    G/T is the key parameter describing receive system quality.
    Higher G/T means better ability to detect weak signals.

    Args:
        antenna_gain_dbi: Antenna gain in dBi. Can be negative.
        system_noise_temp_k: Total system noise temperature in Kelvin.
        Must be > 0.

    Returns:
        G/T in dB/K.

    Raises:
        ValueError: If system_noise_temp_k is not positive finite,
        or antenna_gain_dbi is non-finite.
    """
    validate_finite(antenna_gain_dbi=antenna_gain_dbi)
    validate_positive_finite(system_noise_temp_k=system_noise_temp_k)

    return antenna_gain_dbi - 10 * math.log10(system_noise_temp_k)
