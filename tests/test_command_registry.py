
from app import command_definitions
from app.command_registry import COMMANDS, get_help_text, register_command


def test_commands_registered():
    assert "add" in COMMANDS
    assert "undo" in COMMANDS
    assert "redo" in COMMANDS
    assert "save" in COMMANDS
    assert "exit" in COMMANDS


def test_help_text():
    help_text = get_help_text()

    assert "Available commands" in help_text
    assert "Add two numbers" in help_text
    assert "Undo the last change" in help_text


def test_register_command_decorator():
    @register_command("test_command", "Temporary test command")
    def sample():
        return "working"

    try:
        assert sample() == "working"
        assert COMMANDS["test_command"] == "Temporary test command"
    finally:
        COMMANDS.pop("test_command", None)


def test_all_arithmetic_commands_registered():
    expected = {
        "add", "subtract", "multiply", "divide",
        "power", "root", "modulus", "int_divide",
        "percent", "abs_diff",
    }

    assert expected.issubset(COMMANDS.keys())
