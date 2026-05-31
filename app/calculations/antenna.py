import math
from .constants import ANTENNA_GAIN_CONSTANT
from ..validation.validators import validate_positive_finite, validate_range


def calculate_antenna_gain(
    diameter_m: float,
    frequency_ghz: float,
    efficiency: float = 0.65,
) -> float:
    """
    Calculate parabolic antenna gain.

    Args:
        diameter_m: Antenna diameter in meters. Must be > 0.
        frequency_ghz: Signal frequency in GHz. Must be > 0.
        efficiency: Antenna efficiency factor (0 to 1, default 0.65).
            Cannot be exactly 0 — log10(0) is undefined.

    Returns:
        Antenna gain in dBi.

    Raises:
        ValueError: If any parameter fails validation.
    """
    validate_positive_finite(diameter_m=diameter_m, frequency_ghz=frequency_ghz)
    # efficiency=0 produces log10(0) = -inf, so minimum is 0.0001
    validate_range(efficiency, 0.0001, 1.0, "efficiency")

    return (
        20 * math.log10(diameter_m)
        + 20 * math.log10(frequency_ghz)
        + 10 * math.log10(efficiency)
        + ANTENNA_GAIN_CONSTANT
    )