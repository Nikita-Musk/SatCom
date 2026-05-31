import math
from .constants import FSPL_CONSTANT
from ..validation.validators import validate_positive_finite


def calculate_fspl(
    frequency_ghz: float,
    distance_km: float,
) -> float:
    """
    Calculate Free Space Path Loss (FSPL).

    Args:
        frequency_ghz: Signal frequency in GHz. Must be > 0.
        distance_km: Link distance in kilometers. Must be > 0.

    Returns:
        Free space path loss in dB (always positive).

    Raises:
        ValueError: If frequency_ghz or distance_km are not positive finite numbers.
    """
    validate_positive_finite(frequency_ghz=frequency_ghz, distance_km=distance_km)

    return (
        FSPL_CONSTANT
        + 20 * math.log10(frequency_ghz)
        + 20 * math.log10(distance_km)
    )