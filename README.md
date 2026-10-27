# Enhanced Python Calculator Command-Line Application

## Project Overview

The Enhanced Python Calculator is an interactive command-line application developed using Python, Object-Oriented Programming (OOP), and design patterns.

The project demonstrates how to build a modular, maintainable, and well-tested Python application. It supports basic and advanced arithmetic operations, calculation history, undo and redo, logging, automatic saving, and environment-based configuration.

The application also includes automated testing with pytest and Continuous Integration (CI) using GitHub Actions.

## Features

- **10 Arithmetic Operations:** Basic and advanced mathematical calculations.
- **Interactive REPL:** Users can enter commands and perform calculations.
- **Factory Pattern:** Creates the correct arithmetic operation.
- **Memento Pattern:** Supports undo and redo of calculation history changes.
- **Observer Pattern:** Supports calculation logging and automatic history saving.
- **Decorator Pattern:** Automatically registers commands for the help menu.
- **Color-Coded Terminal Output:** Uses colorama to display successful operations in green, errors in red,informational messages in cyan, and warnings in yellow.
- **pandas History Management:** Saves and loads calculation history using CSV files.
- **Input Validation:** Validates numeric input and applies configurable limits.
- **Error Handling:** Handles invalid input, calculation errors, and CSV file errors.
- **Environment Configuration:** Uses `.env` settings to configure the application.
- **Automated Testing:** Uses pytest and pytest-cov.
- **GitHub Actions:** Automatically runs tests and checks code coverage.

## Project Structure

```text
enhanced-python-calculator/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── command_definitions.py
│   ├── command_registry.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   ├── operations.py
│   └── terminal_colors.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_calculation.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_command_registry.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_observers.py
│   ├── test_operations.py
│   └── test_terminal_colors.py
├── .github/
│   └── workflows/
│       └── python-app.yml
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- pandas
- python-dotenv
- pytest
- pytest-cov
- Git and GitHub
- GitHub Actions
- colorama

## Installation and Setup

### 1. Clone the repository

```bash
git clone git@github.com:rajaramnpatil/enhanced-python-calculator.git
cd enhanced-python-calculator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment.

On Linux, macOS, or WSL:

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

.env is for your reference to configure environment variables used in the application.
Update the values if needed.

## Running the Calculator

From the project root directory, run:

```bash
python -m app.calculator
```

The application displays:

```text
Welcome to Enhanced Python Calculator!
Type 'help' to see available commands.
```

Enter `help` to view the available commands.

## Supported Arithmetic Operations

| Command      | Description         | Example               |
| ------------ | ------------------- | --------------------- |
| `add`        | Addition            | 10 + 5 = 15           |
| `subtract`   | Subtraction         | 10 - 5 = 5            |
| `multiply`   | Multiplication      | 10 × 5 = 50           |
| `divide`     | Division            | 10 ÷ 5 = 2            |
| `power`      | Exponentiation      | 2³ = 8                |
| `root`       | Nth root            | √16 = 4               |
| `modulus`    | Remainder           | 10 % 3 = 1            |
| `int_divide` | Integer division    | 10 // 3 = 3           |
| `percent`    | Percentage          | (25 / 100) × 100 = 25 |
| `abs_diff`   | Absolute difference | \|10 - 15\| = 5       |

Each arithmetic command accepts two numeric inputs.

## Other Calculator Commands

| Command   | Description                         |
| --------- | ----------------------------------- |
| `help`    | Display available commands          |
| `history` | Show calculation history            |
| `clear`   | Clear calculation history           |
| `undo`    | Undo the last history change        |
| `redo`    | Redo the last undone history change |
| `save`    | Save calculation history to CSV     |
| `load`    | Load calculation history from CSV   |
| `exit`    | Close the calculator                |

## Example Usage

```text
Welcome to Enhanced Python Calculator!
Type 'help' to see available commands.

Enter command: add
Enter first number: 10
Enter second number: 5
Result: 15.0

Enter command: multiply
Enter first number: 4
Enter second number: 3
Result: 12.0

Enter command: history
1. add(10.0, 5.0) = 15.0
2. multiply(4.0, 3.0) = 12.0

Enter command: undo
Undo successful.

Enter command: redo
Redo successful.

Enter command: save
History saved successfully.

Enter command: exit
Goodbye!
```

## Design Patterns

### 1. Factory Pattern

The Factory pattern is implemented in `operations.py`.

It creates the correct operation based on the command entered by the user. This keeps arithmetic logic separate from the main calculator.

### 2. Memento Pattern

The Memento pattern is implemented in `calculator_memento.py`.

It saves previous states of calculation history so users can undo and redo changes.

### 3. Observer Pattern

The Observer pattern is implemented using `observers.py` and `logger.py`.

The calculator notifies observers when important events occur.

- `LoggingObserver` records application events.
- `AutoSaveObserver` automatically saves history when enabled.

### 4. Decorator Pattern — Optional Feature

The Decorator pattern is implemented in `command_registry.py` and `command_definitions.py`.

It automatically registers command descriptions for the help menu.

This makes it easier to maintain the help menu without manually updating the displayed list.

The Decorator pattern was implemented as an optional feature for the project.

## Logging

The calculator uses Python's built-in `logging` module to record application activities and errors.

- Logging is configured in `app/logger.py`.
- The **Observer Pattern** is used through `LoggingObserver` to record calculator events.
- Important events such as calculations, undo/redo, and history changes are logged.
- Errors during CSV save/load operations are also recorded.
- Log files are stored in the configured `logs/` directory.

Logging settings can be managed through environment variables:

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_LOG_FILE=calculator.log
```

Logging helps with debugging, tracking application activities, and identifying errors without changing the calculator's main logic.

## Calculation History and CSV

The application uses pandas to save and load calculation history.

Each saved record includes:

- Operation name
- First operand
- Second operand
- Result
- Timestamp

The history file is stored in the configured history directory.

When automatic saving is enabled, the calculator saves history after supported history-changing events.

Users can also manually save or load history using the `save` and `load` commands.

The application validates CSV files and handles errors such as missing columns, invalid numbers, incorrect results, and file-access failures.

## Environment Configuration

The application supports the following settings:

```dotenv
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_LOG_FILE=calculator.log
CALCULATOR_HISTORY_FILE=history.csv
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=6
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

| Setting                       | Purpose                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| `CALCULATOR_LOG_DIR`          | Directory for application logs                                  |
| `CALCULATOR_HISTORY_DIR`      | Directory for calculation history                               |
| `CALCULATOR_LOG_FILE`         | Log filename                                                    |
| `CALCULATOR_HISTORY_FILE`     | CSV history filename                                            |
| `CALCULATOR_MAX_HISTORY_SIZE` | Maximum number of calculations retained after a new calculation |
| `CALCULATOR_AUTO_SAVE`        | Enable or disable automatic history saving                      |
| `CALCULATOR_PRECISION`        | Configured precision value                                      |
| `CALCULATOR_MAX_INPUT_VALUE`  | Maximum allowed absolute input value                            |
| `CALCULATOR_DEFAULT_ENCODING` | Encoding used for CSV files                                     |

The current REPL uses the configured input limit and history limit. The precision setting is available in configuration, but the displayed result is not yet formatted using this value.

## Input Validation and Error Handling

The calculator checks that user inputs are valid numbers and within the configured maximum value.

It also handles invalid commands and arithmetic errors.

For CSV history operations, the application uses a custom `HistoryError` exception. When a save or load fails, the calculator displays an error message and logs the failure.

A failed CSV load does not replace the existing calculation history.

## Optional Features

1. Dynamic Help Menu (Decorator Pattern)

Uses the Decorator Pattern to automatically register commands and display them in the help menu.

Makes it easier to add new commands without manually updating the help menu.

Implemented in app/command_registry.py and app/command_definitions.py.

2. Color-Coded Terminal Output (colorama)

Uses the colorama library to improve terminal readability.

Green: Successful operations.

Red: Errors and invalid commands.

Cyan: Welcome and informational messages.

Yellow: Warnings.

Implemented in app/terminal_colors.py.

Both optional features are covered by automated tests.

## Automated Testing

The application uses pytest for automated testing.

To run all tests:

```bash
python -m pytest tests/ -v
```

To run tests with coverage:

```bash
python -m pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-fail-under=90
```

Latest local test results:

- **124 tests passed**
- **98.10% code coverage**
- **90% minimum coverage requirement achieved**

Tests cover arithmetic operations, configuration, input validation, calculation history, design patterns, REPL commands, and CSV error handling.

## GitHub Actions Continuous Integration

GitHub Actions is configured in:

```text
.github/workflows/python-app.yml
```

The workflow runs automatically on configured pushes and pull requests.

It performs the following tasks:

1. Checks out the project.
2. Sets up Python.
3. Installs dependencies.
4. Runs pytest.
5. Checks that code coverage is at least 90%.
6. Uploads the coverage report artifact.

## Git Development Workflow

The project was developed using separate feature branches.

Each major feature was implemented and tested before being merged into the `main` branch.

This approach helps track changes, maintain a clear Git history, and reduce integration issues.

## Conclusion

This project helped me apply Python OOP concepts and design patterns in a practical application.

I learned how to organize code into separate modules, implement undo and redo, manage CSV data using pandas, use environment configuration, handle errors, and write automated tests.

I also gained experience using Git branches, merging features, and running tests automatically through GitHub Actions.

The final application demonstrates modular Python development, automated testing, and maintainable application design.
