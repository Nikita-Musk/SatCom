import math
import pytest
from app.validation.validators import (
    validate_finite,
    validate_non_negative,
    validate_positive,
    validate_positive_finite,
    validate_range,
)


class TestValidatePositive:
    def test_accept_positive_int(self):
        validate_positive(x=1)
    
    def test_accept_positive_float(self):
        validate_positive(x=0.0001)

    def test_accept_multiple_params(self):
        validate_positive(diameter=1.2, frequency=12.0)
    
    def test_rejects_zero(self):
        with pytest.raises(ValueError, match="must be > 0"):
            validate_positive(x=0)

    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="must be > 0"):
            validate_positive(x=-0.001)
    
    def test_rejects_inf(self):
        with pytest.raises(ValueError):
            validate_positive(x=math.inf)

    def test_rejects_nan(self):
        with pytest.raises(ValueError):
            validate_positive(x=math.nan)

    def test_rejects_bool_true(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive(x=True)

    def test_rejects_bool_false(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive(x=False)

    def test_rejects_string(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive(x="-1.5")

    def test_rejects_none(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive(x=None)

    def test_error_contains_param_name(self):
        with pytest.raises(ValueError, match="diameter_m"):
            validate_positive(diameter_m=-5)
    
    def test_error_contains_value(self):
        with pytest.raises(ValueError, match="-5.0"):
            validate_positive(x=-5.0)


class TestValidateNonNegative:
    def test_accepts_zero(self):
        validate_non_negative(x=0)

    def test_accepts_zero_float(self):
        validate_non_negative(x=0.0)

    def test_accepts_positive(self):
        validate_non_negative(x=1.5)
    
    def test_rejects_negative(self):
        with pytest.raises(ValueError, match="must be >= 0"):
            validate_non_negative(x=-0.0001)

    def test_rejects_bool(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_non_negative(losses_db=True)

class TestValidateRange:
    def test_accepts_min_boundary(self):
        validate_range(0.0001, 0.0001, 1.0, "efficiency")

    def test_accepts_max_boundary(self):
        validate_range(1.0, 0.0001, 1.0, "efficiency")

    def test_accepts_middle_value(self):
        validate_range(0.65, 0.0001, 1.0, "efficiency")

    def test_rejects_below_min(self):
        with pytest.raises(ValueError, match="\[0.0001, 1.0\]"):
            validate_range(0.000009, 0.0001, 1.0, "efficiency")

    def test_rejects_above_max(self):
        with pytest.raises(ValueError, match="efficiency"):
            validate_range(1.001, 0.0001, 1.0, "efficiency")

    def test_rejects_nan(self):
        with pytest.raises(ValueError):
            validate_range(math.nan, 0.0001, 1.0, "efficiency")
            
    def test_rejects_inf(self):
        with pytest.raises(ValueError):
            validate_range(math.inf, 0.0001, 1.0, "efficiency")

class TestValidateFinite:
    def test_accepts_negative(self):
        validate_finite(gain_db=-3.0)
    
    def test_accepts_zero(self):
        validate_finite(x=0.0)

    def test_rejects_inf(self):
        with pytest.raises(ValueError):
            validate_finite(x=math.inf)
    
    def test_rejects_negative_ing(self):
        with pytest.raises(ValueError):
            validate_finite(x=-math.inf)

    def test_rejects_nan(self):
        with pytest.raises(ValueError):
            validate_finite(x=math.nan)

class TestValidatePositiveFinite:
    def test_accepts_valid_values(self):
        validate_positive_finite(diameter_m=1.2, frequency_ghz=12.0)

    @pytest.mark.parametrize("bad_value", [
        0, 0.0, -1, -0.001,
        math.inf, -math.inf, math.nan,
        True, False, "1.0", None, [], {}
    ])
    def test_rejects_invalid_values(self, bad_value):
        with pytest.raises(ValueError):
            validate_positive_finite(frequency_ghz=bad_value)
    
    def test_error_contains_param_name(self):
        with pytest.raises(ValueError, match="frequency_ghz"):
            validate_positive_finite(frequency_ghz=-1.2)

    def test_error_contains_value(self):
        with pytest.raises(ValueError, match="-2.0"):
            validate_positive_finite(frequency_ghz=-2.0)

    def test_rejects_bool(self):
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive_finite(frequency_ghz=True)

    def test_rejects_negative_value(self):
        with pytest.raises(ValueError, match="must be > 0"):
            validate_positive_finite(frequency_ghz=-1.0)
    