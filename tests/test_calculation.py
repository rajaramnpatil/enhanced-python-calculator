
import pytest

from app.calculation import Calculation


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 5, 5),
        ("multiply", 10, 5, 50),
        ("divide", 10, 5, 2),
        ("power", 2, 3, 8),
        ("root", 16, 2, 4),
        ("modulus", 10, 3, 1),
        ("int_divide", 10, 3, 3),
        ("percent", 25, 100, 25),
        ("abs_diff", 10, 15, 5),
    ],
)
def test_calculation(operation, a, b, expected):
    calculation = Calculation(operation, a, b)

    assert calculation.result == pytest.approx(expected)
    assert calculation.operation == operation
    assert calculation.operand1 == a
    assert calculation.operand2 == b
    assert calculation.timestamp is not None


def test_invalid_calculation():
    with pytest.raises(ValueError):
        Calculation("unknown", 10, 5)


def test_calculation_division_by_zero():
    with pytest.raises(ValueError):
        Calculation("divide", 10, 0)
