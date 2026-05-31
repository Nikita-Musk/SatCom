""" 
тестовая тема по идее должна идти перед расчетом g/t
noise_figure_db (из датащита)
        ↓
calculate_receiver_noise_temperature()  →  receiver_noise_temp_k
        ↓
calculate_system_noise_temperature()    →  system_noise_temp_k
        ↓
calculate_g_over_t()                    →  g/t в дБ/К
        ↓
calculate_cn()                          →  C/N в дБ
"""
from ..validation.validators import validate_non_negative, validate_positive_finite


def calculate_receiver_noise_temperature(
    noise_figure_db: float,
) -> float:
    """
    Convert receiver noise figure to noise temperature.

    Args:
        noise_figure_db: Receiver noise figure in dB. Must be >= 0.
        0 dB means ideal (noiseless) receiver.

    Returns:
        Equivalent noise temperature in Kelvin.

    Raises:
        ValueError: If noise_figure_db is negative or non-finite.

    Example:
        >>> calculate_receiver_noise_temperature(3.0)
        289.6
    """
    validate_positive_finite(noise_figure_db=noise_figure_db)

    noise_figure_linear = 10 ** (noise_figure_db / 10)
    # Reference temperature T0 = 290 K (ITU-R standard)
    return 290.0 * (noise_figure_linear - 1)


def calculate_system_noise_temperature(
    antenna_noise_temp_k: float,
    receiver_noise_temp_k: float,
    line_loss_db: float = 0.0,
) -> float:
    """
    Calculate total system noise temperature.

    Accounts for antenna noise, feedline losses, and receiver noise.
    Uses Friis formula for cascaded noise.

    Args:
        antenna_noise_temp_k: Antenna noise temperature in Kelvin. Must be > 0.
        receiver_noise_temp_k: Receiver noise temperature in Kelvin. Must be > 0.
        line_loss_db: Feedline loss between antenna and receiver in dB.
        Must be >= 0. Default 0.0 (lossless line).

    Returns:
        Total system noise temperature in Kelvin.

    Raises:
        ValueError: If any parameter fails validation.

    Example:
        >>> calculate_system_noise_temperature(35.0, 289.6, 0.5)
        374.2
    """
    validate_positive_finite(
        antenna_noise_temp_k=antenna_noise_temp_k,
        receiver_noise_temp_k=receiver_noise_temp_k,
    )
    validate_non_negative(line_loss_db=line_loss_db)

    line_loss_linear = 10 ** (line_loss_db / 10)
    # Friis: feedline adds (L-1)*T0 noise, attenuates antenna noise
    feedline_noise = (line_loss_linear - 1) * 290.0
    return (
        antenna_noise_temp_k / line_loss_linear
        + feedline_noise
        + receiver_noise_temp_k
    )
