import pytest
import math
from app.calculations.eirp import calculate_eirp


class TestCalculateEIRP:
    @pytest.mark.parametrize("tx_power_dbw, antenna_gain_dbi, losses_db, expected", [
    (10.0, 41.70, 1.50, 50.20), #test
    (10.0, 41.70, 0.0, 51.70), #zero losses 
    (-3.0,  41.70, 1.50, 37.2), #negative tx power
    (10, -3.0, 0.00, 7.0), #negative antenna gain
    ])
    def test_parametrized_known_results(self, tx_power_dbw, antenna_gain_dbi, losses_db, expected):
        result = calculate_eirp(
            tx_power_dbw=tx_power_dbw,
            antenna_gain_dbi=antenna_gain_dbi,
            losses_db=losses_db)
        assert result == pytest.approx(expected, abs=0.01)
    
    @pytest.mark.parametrize("bad_value", [
        -math.inf, math.inf, math.nan,
        True, False, "1", None, [], {}
    ])
    def test_rejects_invalid_tx_power_values(self, bad_value):
        with pytest.raises(ValueError, match="tx_power_dbw"):
            calculate_eirp(
            tx_power_dbw=bad_value,
            antenna_gain_dbi=41.50,
            losses_db=1.0)
    
    @pytest.mark.parametrize("bad_value", [
        -math.inf, math.inf, math.nan,
        True, False, "1", None, [], {}
    ])
    def test_rejects_invalid_antenna_gain_values(self, bad_value):
        with pytest.raises(ValueError, match="antenna_gain_dbi"):
            calculate_eirp(
            tx_power_dbw=10.0,
            antenna_gain_dbi=bad_value,
            losses_db=1.0)

    @pytest.mark.parametrize("bad_value", [
        -1, -0.001, -math.inf, math.inf, math.nan,
        True, False, "1", None, [], {}
    ])
    def test_rejects_invalid_frequency_values(self, bad_value):
        with pytest.raises(ValueError, match="losses_db"):
            calculate_eirp(
            tx_power_dbw=10.0,
            antenna_gain_dbi=-2.9,
            losses_db=bad_value)