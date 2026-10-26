
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def test_default_configuration(monkeypatch):
    variables = [
        "CALCULATOR_LOG_DIR",
        "CALCULATOR_HISTORY_DIR",
        "CALCULATOR_LOG_FILE",
        "CALCULATOR_HISTORY_FILE",
        "CALCULATOR_MAX_HISTORY_SIZE",
        "CALCULATOR_AUTO_SAVE",
        "CALCULATOR_PRECISION",
        "CALCULATOR_MAX_INPUT_VALUE",
        "CALCULATOR_DEFAULT_ENCODING",
    ]

    for variable in variables:
        monkeypatch.delenv(variable, raising=False)

    config = CalculatorConfig()

    assert config.max_history_size == 100
    assert config.auto_save is True
    assert config.precision == 2
    assert config.max_input_value == 1000000
    assert config.default_encoding == "utf-8"


def test_custom_configuration(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_PRECISION", "4")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")

    config = CalculatorConfig()

    assert config.max_history_size == 50
    assert config.precision == 4
    assert config.auto_save is False


def test_configuration_paths():
    config = CalculatorConfig(
        log_dir="logs",
        history_dir="history",
        log_file="test.log",
        history_file="test.csv",
    )

    assert str(config.log_file_path) == "logs/test.log"
    assert str(config.history_file_path) == "history/test.csv"


@pytest.mark.parametrize(
    "settings",
    [
        {"max_history_size": 0},
        {"max_history_size": -1},
        {"precision": -1},
        {"max_input_value": 0},
        {"max_input_value": -100},
        {"max_input_value": float("nan")},
        {"default_encoding": ""},
    ],
)
def test_invalid_configuration(settings):
    with pytest.raises(ValidationError):
        CalculatorConfig(**settings)
