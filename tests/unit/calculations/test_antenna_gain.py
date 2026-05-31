import pytest 
from app.calculations.antenna import calculate_antenna_gain


class TestCalculateAntennaGain:
    @pytest.mark.parametrize("diameter,frequency,efficiency,expected", [
    (1.2, 12.0, 0.65, 41.70),
    (2.4, 12.0, 0.65, 47.72),  # двойной диаметр → +6.02 dB
    (1.2,  6.0, 0.65, 35.68),  # вдвое меньше частота → -6.02 dB
    ])
    def test_parametrized_known_results(self, diameter, frequency, efficiency, expected):
        result = calculate_antenna_gain(diameter, frequency, efficiency)
        assert result == pytest.approx(expected, abs=0.01)

    def test_default_eddiciency(self):
        result = calculate_antenna_gain(diameter_m=1.2, frequency_ghz=12.0)
        assert result == pytest.approx(41.70, abs=0.01)

    def test_large_antenna_has_higher_gain(self):
        gain_small = calculate_antenna_gain(diameter_m=1.0, frequency_ghz=12.0)
        gaint_large = calculate_antenna_gain(diameter_m=2.0, frequency_ghz=12)
        assert gaint_large > gain_small

    def test_higher_frequency_has_higher_gain(self):
        gain_low = calculate_antenna_gain(diameter_m=1.0, frequency_ghz=11.0)
        gain_high = calculate_antenna_gain(diameter_m=1.0, frequency_ghz=12.0)
        assert gain_high > gain_low

    def test_rejects_zero_diameter(self):
        with pytest.raises(ValueError, match="diameter_m"):
            calculate_antenna_gain(diameter_m=0, frequency_ghz=12.0)

    def test_rejects_negatve_frequency(self):
        with pytest.raises(ValueError, match="frequency_ghz"):
            calculate_antenna_gain(diameter_m=1.0, frequency_ghz=-12.0)
    
    def test_rejects_zero_efficiency(self):
        with pytest.raises(ValueError, match="efficiency"):
            calculate_antenna_gain(diameter_m=1.0, frequency_ghz=12.0, efficiency=0.0)
        
    def test_rejects_efficiency_above_one(self):
        with pytest.raises(ValueError, match="efficiency"):
            calculate_antenna_gain(diameter_m=1.0, frequency_ghz=12.0, efficiency=1.01)
