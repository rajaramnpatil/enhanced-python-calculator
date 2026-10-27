
from colorama import Fore, Style, just_fix_windows_console


class TerminalColors:
    """Provide colored terminal messages."""

    @staticmethod
    def initialize():
        """Enable ANSI color support on Windows terminals."""
        just_fix_windows_console()

    @staticmethod
    def success(message):
        """Returns a green colored success message."""
        return f"{Fore.GREEN}{message}{Style.RESET_ALL}"

    @staticmethod
    def error(message):
        """Returns a red colored error message."""
        return f"{Fore.RED}{message}{Style.RESET_ALL}"

    @staticmethod
    def info(message):
        """Returns a cyan colored informational message."""
        return f"{Fore.CYAN}{message}{Style.RESET_ALL}"

    @staticmethod
    def warning(message):
        """Returns a yellow colored warning message."""
        return f"{Fore.YELLOW}{message}{Style.RESET_ALL}"
