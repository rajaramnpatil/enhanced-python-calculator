
from colorama import Fore, Style
from app.terminal_colors import TerminalColors
from unittest.mock import patch


def test_initialize():
    with patch(
        "app.terminal_colors.just_fix_windows_console"
    ) as mocked_initialize:
        TerminalColors.initialize()

    mocked_initialize.assert_called_once()


def test_success_message():
    result = TerminalColors.success("Calculation successful")
    assert result == (
        f"{Fore.GREEN}Calculation successful{Style.RESET_ALL}"
    )


def test_error_message():
    result = TerminalColors.error("Invalid input")
    assert result == (
        f"{Fore.RED}Invalid input{Style.RESET_ALL}"
    )


def test_info_message():
    result = TerminalColors.info("Welcome")
    assert result == (
        f"{Fore.CYAN}Welcome{Style.RESET_ALL}"
    )


def test_warning_message():
    result = TerminalColors.warning("No history")
    assert result == (
        f"{Fore.YELLOW}No history{Style.RESET_ALL}"
    )


def test_initialize():
    with patch(
        "app.terminal_colors.just_fix_windows_console"
    ) as mocked_initialize:
        TerminalColors.initialize()

    mocked_initialize.assert_called_once()
