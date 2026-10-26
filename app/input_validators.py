
import math

from app.exceptions import ValidationError


class InputValidator:
    """ This class validates numerical input for calculator operations."""

    DEFAULT_MAX_VALUE = 1_000_000

    @staticmethod
    def validate_number(value, max_value=DEFAULT_MAX_VALUE):
        try:
            number = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                "Invalid input. Please enter a valid number."
            ) from None

        if not math.isfinite(number):
            raise ValidationError(
                "Input must be a finite number."
            )

        if abs(number) > max_value:
            raise ValidationError(
                f"Input must be between {-max_value} and {max_value}."
            )

        return number
