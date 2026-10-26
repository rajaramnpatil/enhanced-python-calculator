
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

@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("power", 2, 3, 8),
        ("power", 2, -2, 0.25),
        ("power", 5, 0, 1),
        ("root", 27, 3, 3),
        ("root", 16, 2, 4),
        ("root", -27, 3, -3),
        ("modulus", 10, 3, 1),
        ("modulus", 15, 4, 3),
        ("int_divide", 10, 3, 3),
        ("int_divide", -10, 3, -4),
        ("percent", 25, 100, 25),
        ("percent", 50, 200, 25),
        ("abs_diff", 10, 15, 5),
        ("abs_diff", -10, 5, 15),
    ],
)
def test_advanced_operations(operation, a, b, expected):
    operation_instance = OperationFactory.create_operation(operation)
    result = operation_instance.calculate(a, b)

    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "operation,a,b",
    [
        ("root", 16, 0),
        ("root", -16, 2),
        ("root", 0, -2),
        ("modulus", 10, 0),
        ("int_divide", 10, 0),
        ("percent", 10, 0),
        ("power", -4, 0.5),
    ],
)
def test_advanced_operation_errors(operation, a, b):
    operation_instance = OperationFactory.create_operation(operation)

    with pytest.raises(ValueError):
        operation_instance.calculate(a, b)
