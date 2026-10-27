
"""Decorator-based command registration for calculator help."""

COMMANDS = {}


def register_command(name, description):
    """Register a calculator command and its description."""

    def decorator(func):
        COMMANDS[name] = description
        return func

    return decorator


def get_help_text():
    """Build the help menu from registered commands."""
    lines = ["Available commands:"]

    for name, description in COMMANDS.items():
        lines.append(f"  {name:<12} - {description}")

    return "\n".join(lines)
