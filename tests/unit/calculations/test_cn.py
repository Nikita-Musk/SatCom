import pytest
import math
from app.calculations.cn import calculate_cn


class TestCalculateCN:
    def test_know_result(self):
        result = calculate_cn(
            eirp_dbw=50.2,
            fspl_db=168.01,
            g_over_t_db_k=16.20,
            bandwidth_hz=36e6,
            additional_losses_db=0.0,
        )
        assert result == pytest.approx(51.43, abs=0.01)

    def test_higher_eirp_improves_cn_by_same_amount(self):
        cn_base = calculate_cn(50.2, 168.01, 16.20, 36e6)
        cn_better = calculate_cn(53.2, 168.01, 16.20, 36e6)
        assert (cn_better - cn_base) == pytest.approx(3.0, abs=0.01)

    def test_additional_losses_reduce_cn(self):
        cn_no_loss = calculate_cn(50.2, 168.01, 16.20, 36e6, 0.0)
        cn_with_loss = calculate_cn(50.2, 168.01, 16.20, 36e6, 3.0)
        assert (cn_no_loss - cn_with_loss) == pytest.approx(3.0, abs=0.01)

    def test_wider_bandwidth_reduces_cn(self):
        cn_narrow = calculate_cn(50.2, 168.01, 16.20, 36e6)
        cn_wide = calculate_cn(50.2, 168.01, 16.20, 72e6)
        # двойная полоса → -3 dB
        assert (cn_narrow - cn_wide) == pytest.approx(3.01, abs=0.01)

    def test_default_additional_losses_is_zero(self):
        cn_default = calculate_cn(50.2, 168.01, 16.20, 36e6)
        cn_explicit = calculate_cn(50.2, 168.01, 16.20, 36e6, 0.0)
        assert cn_default == pytest.approx(cn_explicit, abs=0.001)
    
    def test_accepts_negative_eirp(self):
        # eirp может быть отрицательным в дБ
        result = calculate_cn(-10.0, 168.01, 16.20, 36e6)
        assert isinstance(result, float)

    def test_accepts_negative_g_over_t(self):
        result = calculate_cn(50.2, 168.01, -5.0, 36e6)
        assert isinstance(result, float)

    def test_rejects_zero_bandwidth(self):
        with pytest.raises(ValueError, match="bandwidth_hz"):
            calculate_cn(50.2, 168.01, 16.20, 0.0)

    def test_rejects_zero_fspl(self):
        with pytest.raises(ValueError, match="fspl_db"):
            calculate_cn(50.2, 0.0, 16.20, 36e6)

    def test_rejects_negative_losses(self):
        with pytest.raises(ValueError, match="additional_losses_db"):
            calculate_cn(50.2, 168.01, 16.20, 36e6, -1.0)

    def test_rejects_inf_eirp(self):
        with pytest.raises(ValueError):
            calculate_cn(math.inf, 168.01, 16.20, 36e6)
        
    def test_rejects_nan_bandwidth(self):
        with pytest.raises(ValueError):
            calculate_cn(50.2, 168.01, 16.20, math.nan)
            