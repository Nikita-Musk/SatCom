import math 
import numbers


def _check_type(value: float, name:str) -> None:
    """Checking for non-bool types, only numeric types"""
    if isinstance(value, bool) or not isinstance(value, numbers.Real):
        raise ValueError(
            f"Parameter '{name}' must be a number, got {type(value).__name__}"
        )

def _base_validate(value: float, name: str, allow_zero: bool) -> None:
    """Base validator type → limb → sign"""
    _check_type(value, name)
    if not math.isfinite(value):
        raise ValueError(
            f"Parameter '{name}' must be finity, got {value}"
        )
    if allow_zero:
        if value < 0:
            raise ValueError(
                f"Parameter '{name}' must be >= 0, got {value}"
            )
    else:
        if value <= 0:
            raise ValueError(
                f"Parameter '{name}' must be > 0, got {value}"
            )
        
def validate_positive(**kwargs: float) -> None:
    """All values > 0"""
    for name, value in kwargs.items():
        _base_validate(value, name, allow_zero=False)

def validate_non_negative(**kwargs: float) -> None:
    """All values >= 0"""
    for name, value in kwargs.items():
        _base_validate(value, name, allow_zero=True)

def validate_finite(**kwargs: float) -> None:
    """All values are finite (but may be negative)"""
    for name, value in kwargs.items():
        _check_type(value, name)
        if not math.isfinite(value):
            raise ValueError(
                f"Parameter {name} must be finite, got {value}"
            )

def validate_positive_finite(**kwargs: float) -> None:
    """All values > 0 and finite, Combo for physical quantities"""
    for name, value in kwargs.items():
        _base_validate(value, name, allow_zero=False)

def validate_range(
        value: float,
        min_val: float,
        max_val: float,
        name: str
) -> None:
    """Value in range [min_val, max_val]"""
    _check_type(value, name)
    if not math.isfinite(value):
        raise ValueError(
            f"Parameter '{name}' must be finite,fot {value}"
        )
    if not (min_val <= value <=max_val):
        raise ValueError(
            f"Parameter '{name}' must be in [{min_val}, {max_val}], got{value}"
        )
    