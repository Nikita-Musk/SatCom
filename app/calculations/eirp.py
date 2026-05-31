from ..validation.validators import validate_finite, validate_non_negative


def calculate_eirp(
    tx_power_dbw: float,
    antenna_gain_dbi: float,
    losses_db: float,
) -> float:
    """
    Calculate Effective Isotropic Radiated Power (EIRP).

    Args:
        tx_power_dbw: Transmitter output power in dBW.
            Can be negative (e.g. -3 dBW = 0.5 W).
        antenna_gain_dbi: Antenna gain in dBi.
            Can be negative for lossy antennas.
        losses_db: Total transmission losses in dB. Must be >= 0.
            Includes cable, connector, and atmospheric losses.

    Returns:
        EIRP in dBW.

    Raises:
        ValueError: If losses_db is negative or any value is non-finite.
    """
    validate_finite(tx_power_dbw=tx_power_dbw, antenna_gain_dbi=antenna_gain_dbi)
    validate_non_negative(losses_db=losses_db)

    return tx_power_dbw + antenna_gain_dbi - losses_db