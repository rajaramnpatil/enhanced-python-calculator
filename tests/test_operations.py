
import pytest

from app.operations import OperationFactory


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("add", -10, 5, -5),
        ("multiply", -2, 5, -10),
        ("divide", 5, 2, 2.5),
    ],
)
def test_operations(operation, a, b, expected):
    operation_instance = OperationFactory.create_operation(operation)
    result = operation_instance.calculate(a, b)

    assert result == pytest.approx(expected)


def test_division_by_zero():
    operation = OperationFactory.create_operation("divide")

    with pytest.raises(ValueError, match="Cannot divide by zero"):
        operation.calculate(10, 0)


def test_invalid_operation():
    with pytest.raises(ValueError, match="Unsupported operation"):
        OperationFactory.create_operation("invalid")
