
from app.calculator_memento import CalculatorCaretaker
from app.input_validators import InputValidator
from app.exceptions import ValidationError

from app.calculation import Calculation
from app.operations import OperationFactory


class Calculator:
    """Enhanced Interactive command-line calculator."""

    def __init__(self):
        self.history = []
        self.caretaker = CalculatorCaretaker()

    def perform_calculation(self, operation, a, b):
        calculation = Calculation(operation, a, b)

        # Save history only after a successful calculation.
        self.caretaker.save_state(self.history)

        self.history.append(calculation)
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
        print("\nAvailable commands:")
        for operation in OperationFactory._operations:
            print(f"  {operation}")

        print("  history")
        print("  clear")
        print("  help")
        print("  undo")
        print("  redo")
        print("  exit")

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

                    print("Calculation history cleared.")

                elif command == "undo":
                    self.undo()

                elif command == "redo":
                    self.redo()
                elif command in OperationFactory._operations:
                    a = InputValidator.validate_number(
                    input("Enter first number: ")
                    )

                    b = InputValidator.validate_number(
                    input("Enter second number: ")
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
        print("Undo successful.")


    def redo(self):
        """Redo the last undone history change."""
        next_state = self.caretaker.redo(self.history)

        if next_state is None:
            print("Nothing to redo.")
            return

        self.history = next_state
        print("Redo successful.")


if __name__ == "__main__":
    Calculator().repl()
