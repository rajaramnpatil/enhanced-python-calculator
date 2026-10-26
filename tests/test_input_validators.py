
import pytest

from app.input_validators import InputValidator
from app.exceptions import ValidationError


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10", 10),
        ("-5", -5),
        ("3.14", 3.14),
        ("0", 0),
        ("1000000", 1000000),
    ],
)
def test_valid_numbers(value, expected):
    assert InputValidator.validate_number(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        "",
        None,
        "nan",
        "inf",
        "-inf",
        "1000001",
        "-1000001",
    ],
)
def test_invalid_numbers(value):
    with pytest.raises(ValidationError):
        InputValidator.validate_number(value)
