from utils.exceptions import ValidationError

def validate_range(name: str, value: int, min_val: int, max_val: int) -> int:
    """Ensure value is within min and max, raise ValidationError if not."""
    if not (min_val <= value <= max_val):
        raise ValidationError(
            f"Invalid value for {name}: {value}. Must be between {min_val} and {max_val}."
        )
    return value

def validate_type(name: str, value, expected_type):
    """Ensure value is of correct type."""
    if not isinstance(value, expected_type):
        raise ValidationError(
            f"Invalid type for {name}: expected {expected_type.__name__}, got {type(value).__name__}."
        )
    return value

def validate_choice(name: str, value, valid_choices):
    """Ensure value is one of allowed choices."""
    if value not in valid_choices:
        raise ValidationError(
            f"Invalid value for {name}: {value}. Must be one of {valid_choices}."
        )
    return value
