import pytest
import math
from app.calculations.fspl import calculate_fspl


class TestCalculateFspl:
    @pytest.mark.parametrize("frequency,distance,expected", [
        (12.0, 500.0,   168.01),
        (12.0, 1000.0,  174.03),
        (6.0,  500.0,   161.99),
    ])
    def test_parametrize_known_results(self, frequency, distance, expected):
        result = calculate_fspl(frequency_ghz=frequency, distance_km=distance)
        assert result == pytest.approx(expected, abs=0.01)
    
    def test_double_distance_adds_6db(self):
        fspl_1 = calculate_fspl(frequency_ghz=12.0, distance_km=500.0)
        fspl_2 = calculate_fspl(frequency_ghz=12.0, distance_km=1000.0)
        assert (fspl_2 - fspl_1) == pytest.approx(6.02, abs=0.01)

    def test_double_frequency_adds_6db(self):
        fspl_1 = calculate_fspl(frequency_ghz=6.0, distance_km=500.0)
        fspl_2 = calculate_fspl(frequency_ghz=12.0, distance_km=500.0)
        assert (fspl_2 - fspl_1) == pytest.approx(6.02, abs=0.01)
    
    def test_result_always_positeve(self):
        result = calculate_fspl(frequency_ghz=3, distance_km=300)
        assert result > 0

    @pytest.mark.parametrize("bad_value", [
        0, -1, -0.001, -math.inf, math.inf, math.nan,
        True, False, "1", None, [], {}
    ])
    def test_rejects_invalid_frequency_values(self, bad_value):
        with pytest.raises(ValueError, match="frequency_ghz"):
            calculate_fspl(frequency_ghz=bad_value, distance_km=3.9)

    @pytest.mark.parametrize("bad_value", [
        0, -1, -0.001, -math.inf, math.inf, math.nan,
        True, False, "1", None, [], {}
    ])
    def test_rejects_invalid_distance_values(self, bad_value):
        with pytest.raises(ValueError, match="distance_km"):
            calculate_fspl(frequency_ghz=12.0, distance_km=bad_value)
