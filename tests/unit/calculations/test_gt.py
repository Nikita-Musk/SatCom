import pytest
import math
from app.calculations.gt import calculate_g_over_t

class TestCalculateGOverT:
    def test_known_result(self):
        result = calculate_g_over_t (
            antenna_gain_dbi=41.70,
            system_noise_temp_k=355.17,
        )
        assert result == pytest.approx(16.20, abs=0.01)
    
    def test_higher_gain_improves_g_over_t(self):
        gt_low = calculate_g_over_t(40.0, 355.17)
        gt_high = calculate_g_over_t(46.0, 355.17)
        assert gt_high == pytest.approx(gt_low + 6.0, abs=0.01)

    def test_higher_noise_temp_reduces_g_over_t(self):
        gt_cold = calculate_g_over_t(41.70, 100.0)
        gt_hot = calculate_g_over_t(41.70, 1000.0)
        assert gt_cold > gt_hot

    def test_accepts_negative_antenna_gain(self):
        calculate_g_over_t(antenna_gain_dbi=-3.0, system_noise_temp_k=355.17)

    def test_rejects_zero_noise_temp(self):
        with pytest.raises(ValueError, match="system_noise_temp_k"):
            calculate_g_over_t(antenna_gain_dbi=41.70, system_noise_temp_k=0)
    
    def test_rejects_negative_noise_temp(self):
        with pytest.raises(ValueError, match="system_noise_temp_k"):
            calculate_g_over_t(antenna_gain_dbi=41.70, system_noise_temp_k=-1.0)

    def test_rejects_inf_antenna_gain(self):
        with pytest.raises(ValueError, match="antenna_gain_dbi"):
            calculate_g_over_t(antenna_gain_dbi=math.inf, system_noise_temp_k=355.17)

    def test_rejects_nan_noise_temp(self):
        with pytest.raises(ValueError, match="system_noise_temp_k"):
            calculate_g_over_t(antenna_gain_dbi=41.70, system_noise_temp_k=math.nan)
            