
import math

from app.exceptions import ValidationError


class InputValidator:
    """Validate calculator input values."""

    @staticmethod
    def validate_number(value, max_input_value=1_000_000):
        try:
            number = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                "Invalid number. Please enter a valid numeric value."
            )

        if not math.isfinite(number):
            raise ValidationError(
                "Number must be finite."
            )

        if abs(number) > max_input_value:
            raise ValidationError(
                f"Number exceeds the maximum allowed value: "
                f"{max_input_value}"
            )

        return number
