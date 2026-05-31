import math 
from ..validation.validators import validate_positive_finite, validate_finite


def calculate_watts_to_dbw(power_w: float) -> float:
    """
    Convert power from watts to dBW.

    Args:
        power_w: Power in watts. Must be > 0.
    """
    validate_positive_finite(power_w=power_w)
    return 10 * math.log10(power_w)

def calculate_dbw_to_watts(power_dbw:float) -> float:
    """
    Convert power from dBW to watts.

    Args:
        power_dbw: Power in dBW. Can be negative.
    """
    validate_finite(power_dbw=power_dbw)
    return 10 ** (power_dbw / 10)