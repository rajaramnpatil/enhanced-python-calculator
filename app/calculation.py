
from dataclasses import dataclass, field
from datetime import datetime

from app.operations import OperationFactory


@dataclass
class Calculation:
    """Represents a single calculator operation."""

    operation: str
    operand1: float
    operand2: float
    result: float = field(init=False)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        operation_instance = OperationFactory.create_operation(
            self.operation
        )

        self.result = operation_instance.calculate(
            self.operand1,
            self.operand2
        )
