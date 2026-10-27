
import pytest
from unittest.mock import patch

from app.calculator import Calculator


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
