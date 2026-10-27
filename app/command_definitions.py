
from app.command_registry import register_command


@register_command("add", "Add two numbers")
def add_command():
    pass  # pragma: no cover


@register_command("subtract", "Subtract two numbers")
def subtract_command():
    pass  # pragma: no cover


@register_command("multiply", "Multiply two numbers")
def multiply_command():
    pass  # pragma: no cover


@register_command("divide", "Divide two numbers")
def divide_command():
    pass  # pragma: no cover


@register_command("power", "Raise a number to a power")
def power_command():
    pass  # pragma: no cover


@register_command("root", "Calculate the nth root")
def root_command():
    pass  # pragma: no cover


@register_command("modulus", "Find the remainder")
def modulus_command():
    pass  # pragma: no cover


@register_command("int_divide", "Perform integer division")
def int_divide_command():
    pass  # pragma: no cover


@register_command("percent", "Calculate percentage")
def percent_command():
    pass  # pragma: no cover


@register_command("abs_diff", "Find absolute difference")
def abs_diff_command():
    pass  # pragma: no cover


@register_command("history", "Display calculation history")
def history_command():
    pass  # pragma: no cover


@register_command("clear", "Clear calculation history")
def clear_command():
    pass  # pragma: no cover


@register_command("undo", "Undo the last change")
def undo_command():
    pass  # pragma: no cover


@register_command("redo", "Redo the last undone change")
def redo_command():
    pass  # pragma: no cover


@register_command("save", "Save history to CSV")
def save_command():
    pass  # pragma: no cover


@register_command("load", "Load history from CSV")
def load_command():
    pass  # pragma: no cover


@register_command("help", "Show available commands")
def help_command():
    pass  # pragma: no cover


@register_command("exit", "Exit the calculator")
def exit_command():
    pass  # pragma: no cover
