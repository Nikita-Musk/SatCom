import math
from ..validation.validators import validate_positive_finite, validate_finite, validate_range
from .constants import REQUIRED_EB_N0, MODULATION_ORDER, FEC_RATE_VALUE


def get_required_eb_n0_db(modulation: str, fec_rate: str) -> float:
    """
    Get required Eb/N0 in dB for given modulation and FEC rate.

    Args:
        modulation: Modulation type (e.g. "QPSK").
        fec_rate: FEC code rate (e.g. "3/4").

    Returns:
        Required Eb/N0 in dB.
    """
    key = (modulation, fec_rate)
    if key not in REQUIRED_EB_N0:
        raise ValueError(
            f"Unknown modulation/FEC combination: {modulation} with FEC {fec_rate}. "
            f"Supported combinations: {list(REQUIRED_EB_N0.keys())}"
        )
    return REQUIRED_EB_N0[key]

def calculate_bit_rate_bps(
    bandwidth_hz: float,
    modulation: str,
    fec_rate: str,
    roll_off_factor: float = 0.20
) -> float:
    """
    Calculate bit rate in Bps using DVB-S2 formula.

    Formula:
        BitRate = (BW / (1 + α)) * bits_per_symbol * fec_rate

    where α is the roll-off factor.

    Args:
        bandwidth_mhz: Signal bandwidth in Hz. Must be > 0.
        modulation: Modulation type (BPSK, QPSK, 8PSK, 16APSK, 32APSK).
        fec_rate: FEC code rate (1/2, 2/3, 3/4, 4/5, 7/8).
        roll_off_factor: DVB-S2 roll-off factor α. Must be in [0.05, 0.35].
        Typical values: 0.20 (default), 0.25, 0.35.

    Returns:
        Bit rate in Bps.
    """
    validate_positive_finite(bandwidth_hz=bandwidth_hz)
    validate_range(roll_off_factor, 0.05, 0.35, "roll_off_factor")

    if modulation not in MODULATION_ORDER:
        raise ValueError(
            f"Unknown modulation type: {modulation}. "
            f"Supported types: {list(MODULATION_ORDER.keys())}"
        )
    if fec_rate not in FEC_RATE_VALUE:
        raise ValueError(
            f"Unknown FEC rate: {fec_rate}. "
            f"Supported rates: {list(FEC_RATE_VALUE.keys())}"
        )

    bits_per_symbol = MODULATION_ORDER[modulation]
    fec = FEC_RATE_VALUE[fec_rate]

    return (bandwidth_hz  * bits_per_symbol * fec) / (1 + roll_off_factor)

def calculate_link_margin_db(
    eb_n0_db: float,
    required_eb_n0_db: float,
    implementation_margin_db: float,
) -> float:
    """
    Calculate link margin in dB.

    Args:
        eb_n0_db: Actual Eb/N0 in dB. Can be negative.
        required_eb_n0_db: Required Eb/N0 in dB. Must be > 0.
        implementation_margin_db: Implementation margin in dB. Must be > 0.

    Returns:
        Link margin in dB.
    """
    validate_finite(eb_n0_db=eb_n0_db, required_eb_n0_db=required_eb_n0_db, implementation_margin_db=implementation_margin_db)

    return (
        eb_n0_db 
        - required_eb_n0_db 
        - implementation_margin_db)

def calculate_eb_n0(
    cn0_dbhz: float,
    bit_rate_bps: float,
) -> float:
    """
    Calculate Eb/N0 from C/N0 and bit rate.

    Args:
        cn0_dbhz: Carrier to noise density ratio in dBHz.
        bit_rate_bps: Bit rate in bps. Must be > 0.

    Returns:
        Eb/N0 in dB.
    """
    validate_finite(cn0_dbhz=cn0_dbhz)
    validate_positive_finite(bit_rate_bps=bit_rate_bps)
    return cn0_dbhz - 10 * math.log10(bit_rate_bps)