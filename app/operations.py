
from abc import ABC, abstractmethod


class Operation(ABC):
    """This is the Base class for all calculator operations."""

    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        """Perform a calculation using two numbers."""
        pass


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

class OperationFactory:
    """Creates operation objects based on the operation name."""

    _operations = {
        "add": Add,
        "subtract": Subtract,
        "multiply": Multiply,
        "divide": Divide,
    }

    @classmethod
    def create_operation(cls, operation_name: str) -> Operation:
        operation_class = cls._operations.get(operation_name.lower())

        if operation_class is None:
            raise ValueError(
                f"Unsupported operation: {operation_name}"
            )

        return operation_class()
