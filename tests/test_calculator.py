
from app.calculator_config import CalculatorConfig
import pytest
from unittest.mock import patch

from app.calculator import Calculator
from app.exceptions import HistoryError

from colorama import Fore, Style
from app.terminal_colors import TerminalColors

def test_perform_calculation():
    calculator = Calculator()

    result = calculator.perform_calculation("add", 10, 5)

    assert result == 15
    assert len(calculator.history) == 1


def test_multiple_calculations():
    calculator = Calculator()

    calculator.perform_calculation("add", 10, 5)
    calculator.perform_calculation("multiply", 4, 3)

    assert len(calculator.history) == 2
    assert calculator.history[1].result == 12


def test_show_history(capsys):
    calculator = Calculator()
    calculator.perform_calculation("add", 10, 5)

    calculator.show_history()

    output = capsys.readouterr().out
    assert "add(10, 5) = 15" in output


def test_empty_history(capsys):
    calculator = Calculator()

    calculator.show_history()

    output = capsys.readouterr().out
    assert "No calculation history available" in output


def test_help_command(capsys):
    calculator = Calculator()

    calculator.show_help()

    output = capsys.readouterr().out
    assert "add" in output
    assert "history" in output
    assert "exit" in output


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (["add", "10", "5", "exit"], "Result: 15"),
        (["power", "2", "3", "exit"], "Result: 8"),
        (["invalid", "exit"], "Invalid command"),
        (["divide", "10", "0", "exit"], "Cannot divide by zero"),
        (["add", "abc", "exit"], "Error:"),
        (["history", "exit"], "No calculation history"),
        (["clear", "exit"], "Calculation history cleared"),
        (["help", "exit"], "Available commands"),
    ],
)
def test_repl_commands(inputs, expected, capsys):
    calculator = Calculator()

    with patch("builtins.input", side_effect=inputs):
        calculator.repl()

    output = capsys.readouterr().out
    assert expected in output


def test_repl_keyboard_interrupt(capsys):
    calculator = Calculator()

    with patch("builtins.input", side_effect=KeyboardInterrupt):
        calculator.repl()

    output = capsys.readouterr().out
    assert "Calculator closed" in output


def test_repl_eof(capsys):
    calculator = Calculator()

    with patch("builtins.input", side_effect=EOFError):
        calculator.repl()

    output = capsys.readouterr().out
    assert "Calculator closed" in output

def test_calculator_undo():
    calculator = Calculator()

    calculator.perform_calculation("add", 10, 5)
    calculator.perform_calculation("multiply", 2, 3)

    calculator.undo()

    assert len(calculator.history) == 1
    assert calculator.history[0].result == 15


def test_calculator_redo():
    calculator = Calculator()

    calculator.perform_calculation("add", 10, 5)
    calculator.undo()
    calculator.redo()

    assert len(calculator.history) == 1
    assert calculator.history[0].result == 15


def test_calculator_redo_cleared_after_new_calculation():
    calculator = Calculator()

    calculator.perform_calculation("add", 10, 5)
    calculator.undo()

    calculator.perform_calculation("multiply", 2, 3)
    calculator.redo()

    assert len(calculator.history) == 1
    assert calculator.history[0].operation == "multiply"


def test_undo_redo_repl(capsys):
    calculator = Calculator()

    with patch(
        "builtins.input",
        side_effect=["add", "10", "5", "undo", "redo", "exit"],
    ):
        calculator.repl()

    output = capsys.readouterr().out

    assert "Undo successful" in output
    assert "Redo successful" in output
    assert len(calculator.history) == 1

def test_calculator_auto_save(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=True,
    )

    calculator = Calculator(config)
    calculator.perform_calculation("add", 10, 5)

    assert config.history_file_path.exists()

    loaded = calculator.history_manager.load()

    assert len(loaded) == 1
    assert loaded[0].result == 15


def test_auto_save_after_undo(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=True,
    )

    calculator = Calculator(config)
    calculator.perform_calculation("add", 10, 5)
    calculator.undo()

    assert calculator.history_manager.load() == []


def test_manual_save_and_load(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.perform_calculation("add", 10, 5)

    calculator.save_history()
    calculator.history.clear()
    calculator.load_history()

    assert len(calculator.history) == 1
    assert calculator.history[0].result == 15

def test_max_history_size(tmp_path):
    config = CalculatorConfig(
        max_history_size=2,
        auto_save=False,
        log_dir=tmp_path / "logs",
    )

    calculator = Calculator(config)

    calculator.perform_calculation("add", 1, 2)
    calculator.perform_calculation("multiply", 2, 3)
    calculator.perform_calculation("subtract", 10, 5)

    assert len(calculator.history) == 2
    assert calculator.history[0].operation == "multiply"
    assert calculator.history[1].operation == "subtract"


def test_configured_input_limit(tmp_path):
    config = CalculatorConfig(
        max_input_value=100,
        auto_save=False,
        log_dir=tmp_path / "logs",
    )

    calculator = Calculator(config)

    with patch(
        "builtins.input",
        side_effect=["add", "150", "10", "exit"],
    ):
        calculator.repl()

    assert len(calculator.history) == 0


def test_load_history_error_preserves_existing_history(
    tmp_path, capsys
):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )

    calculator = Calculator(config)
    calculator.perform_calculation("add", 10, 5)

    original_history = calculator.history.copy()

    with patch.object(
        calculator.history_manager,
        "load",
        side_effect=HistoryError("Invalid CSV file"),
    ):
        calculator.load_history()

    assert calculator.history == original_history
    assert "Error loading history" in capsys.readouterr().out


def test_save_history_error_is_handled(tmp_path, capsys):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )

    calculator = Calculator(config)

    with patch.object(
        calculator.history_manager,
        "save",
        side_effect=HistoryError("Permission denied"),
    ):
        calculator.save_history()

    assert "Error saving history" in capsys.readouterr().out


def test_colored_success_message(capsys, tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )
    calculator = Calculator(config)

    calculator.perform_calculation("add", 10, 5)
    calculator.undo()

    output = capsys.readouterr().out

    assert (
        f"{Fore.GREEN}Undo successful.{Style.RESET_ALL}"
        in output
    )


def test_colored_warning_message(capsys, tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )
    calculator = Calculator(config)

    calculator.undo()

    output = capsys.readouterr().out

    assert (
        f"{Fore.YELLOW}Nothing to undo.{Style.RESET_ALL}"
        in output
    )