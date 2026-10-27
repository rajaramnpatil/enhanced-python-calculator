
from abc import ABC, abstractmethod


class Operation(ABC):
    """This is the Base class for all calculator operations."""

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Perform a calculation using two numbers."""
        pass  # pragma: no cover


class Add(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a + b


class Subtract(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a - b


class Multiply(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a * b


class Divide(Operation):
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b


class Power(Operation):
    """Raise a number to a given power."""

    def calculate(self, a: float, b: float) -> float:
        result = a ** b

        if isinstance(result, complex):
            raise ValueError("Complex results are not supported.")

        return result


class Root(Operation):
    """Calculate the nth root of a number."""

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Root degree cannot be zero.")

        if a == 0 and b < 0:
            raise ValueError("Cannot calculate a negative root of zero.")

        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0:
                raise ValueError(
                    "Negative numbers require an odd integer root."
                )
            return -((-a) ** (1 / b))

        return a ** (1 / b)


class Modulus(Operation):
    """Calculate the remainder of division."""

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot calculate modulus by zero.")

        return a % b


class IntegerDivide(Operation):
    """Perform floor division."""

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero.")

        return a // b


class Percent(Operation):
    """Calculate a as a percentage of b."""

    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot calculate percentage with zero.")

        return (a / b) * 100


class AbsoluteDifference(Operation):
    """Calculate the absolute difference."""

    def calculate(self, a: float, b: float) -> float:
        return abs(a - b)

class OperationFactory:
    """Creates operation objects based on the operation name."""

  
    _operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
        "power": Power,
        "root": Root,
        "modulus": Modulus,
        "int_divide": IntegerDivide,
        "percent": Percent,
        "abs_diff": AbsoluteDifference,
    }


    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        operation_class = cls._operations.get(operation_name.lower())

        if operation_class is None:
            raise ValueError(
                f"Unsupported operation: {operation_name}"
            )

        return operation_class()
