
class CalculatorError(Exception):
    """Base exception for calculator errors."""


class ValidationError(CalculatorError):
    """Raised when calculator input is invalid."""


class OperationError(CalculatorError):
    """Raised when a calculation cannot be performed."""

class HistoryError(CalculatorError):
    """Raised when saving or loading calculation history fails."""
    pass