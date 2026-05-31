import math
from .constants import BOLTZMANN_DB
from ..validation.validators import validate_finite, validate_positive_finite, validate_non_negative

def calculate_cn(
        eirp_dbw: float,
        fspl_db: float,
        g_over_t_db_k: float,
        bandwidth_hz: float,
        additional_losses_db: float = 0.0,
) -> float:
    """
    Calculate Carrier-to-Noise Ratio (C/N).

    Full link budget equation:
        C/N = EIRP - FSPL - additional_losses + G/T - k - B

    where k = Boltzmann constant = -228.6 dBW/K/Hz
        B = noise bandwidth in dBHz

    Args:
        eirp_dbw: Effective Isotropic Radiated Power in dBW.
        fspl_db: Free Space Path Loss in dB. Must be > 0.
        g_over_t_db_k: Receive system figure of merit G/T in dB/K.
        bandwidth_hz: Noise bandwidth in Hz. Must be > 0.
        additional_losses_db: Rain fade, pointing loss, etc. in dB.
        Must be >= 0. Default 0.0.

    Returns:
        C/N in dB.

    Raises:
        ValueError: If any parameter fails validation.
    """
    validate_finite(eirp_dbw=eirp_dbw, g_over_t_db_k=g_over_t_db_k)
    validate_positive_finite(bandwidth_hz=bandwidth_hz, fspl_db=fspl_db)
    validate_non_negative(additional_losses_db=additional_losses_db)

    bandwidth_db = 10 * math.log10(bandwidth_hz)

    return (
        eirp_dbw
        - fspl_db
        - additional_losses_db
        + g_over_t_db_k
        - BOLTZMANN_DB
        - bandwidth_db
    )