
from app import command_definitions
from app.command_registry import get_help_text

from app.calculator_config import CalculatorConfig
from app.history import HistoryManager
from app.logger import setup_logger, LoggingObserver
from app.observers import CalculatorSubject, AutoSaveObserver

from app.calculator_memento import CalculatorCaretaker
from app.input_validators import InputValidator
from app.exceptions import ValidationError

from app.calculation import Calculation
from app.operations import OperationFactory


class Calculator:
    """Enhanced Interactive command-line calculator."""

    
    def __init__(self, config=None):
        self.config = config or CalculatorConfig()
        self.history = []
        self.caretaker = CalculatorCaretaker()

        self.subject = CalculatorSubject()

        self.logger = setup_logger(self.config)
        self.subject.attach(LoggingObserver(self.logger))

        self.history_manager = HistoryManager(self.config)

        if self.config.auto_save:
            self.subject.attach(
                AutoSaveObserver(
                    self.history_manager,
                    lambda: self.history,
                )
            )


    
    def perform_calculation(self, operation, a, b):
        calculation = Calculation(operation, a, b)

        self.caretaker.save_state(self.history)
        self.history.append(calculation)

        # Keep only the latest configured number of calculations.
        if len(self.history) > self.config.max_history_size:
            self.history = self.history[
                -self.config.max_history_size:
            ]

        self.subject.notify("calculation", calculation)

        return calculation.result


    def show_history(self):
        if not self.history:
            print("No calculation history available.")
            return

        for index, calculation in enumerate(self.history, start=1):
            print(
                f"{index}. {calculation.operation}"
                f"({calculation.operand1}, "
                f"{calculation.operand2})"
                f" = {calculation.result}"
            )

    def show_help(self):
        """Display automatically registered commands."""
        print(get_help_text())

    def repl(self):
        print("\nWelcome to Enhanced Python Calculator!")
        print("Type 'help' to see available commands.")

        while True:
            try:
                command = input("\nEnter command: ").strip().lower()

                if command == "exit":
                    print("Goodbye!")
                    break

                elif command == "help":
                    self.show_help()

                elif command == "history":
                    self.show_history()

                elif command == "clear":
                    if self.history:
                        self.caretaker.save_state(self.history)
                        self.history.clear()
                        self.subject.notify("clear")

                    print("Calculation history cleared.")

                elif command == "undo":
                    self.undo()

                elif command == "redo":
                    self.redo()

                elif command == "save":
                    self.save_history()

                elif command == "load":
                    self.load_history()

                elif command in OperationFactory._operations:
                    a = InputValidator.validate_number(
                    input("Enter first number: "),
                    self.config.max_input_value,
                    )

                    b = InputValidator.validate_number(
                    input("Enter second number: "),
                    self.config.max_input_value,
                    )

                    result = self.perform_calculation(
                        command, a, b
                    )
                    print(f"Result: {result}")

                else:
                    print("Invalid command. Type 'help'.")

            except (ValueError, ValidationError) as error:
                print(f"Error: {error}")

            except (KeyboardInterrupt, EOFError):
                print("\nCalculator closed.")
                break
    
    def undo(self):
        """Undo the last history change."""
        previous = self.caretaker.undo(self.history)

        if previous is None:
            print("Nothing to undo.")
            return

        self.history = previous
        self.subject.notify("undo")
        print("Undo successful.")


    def redo(self):
        """Redo the last undone history change."""
        next_state = self.caretaker.redo(self.history)

        if next_state is None:
            print("Nothing to redo.")
            return

        self.history = next_state
        self.subject.notify("redo")
        print("Redo successful.")
    
    def save_history(self):
        """Manually save history to CSV."""
        self.history_manager.save(self.history)
        print("History saved successfully.")


    def load_history(self):
        """Load history from CSV."""
        loaded_history = self.history_manager.load()

        # Allow undo after loading a different history.
        if loaded_history != self.history:
            self.caretaker.save_state(self.history)
            self.history = loaded_history

        print("History loaded successfully.")


if __name__ == "__main__":
    Calculator().repl()
