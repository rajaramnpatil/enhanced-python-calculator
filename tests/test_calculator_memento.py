
from app.calculator_memento import CalculatorCaretaker


def test_undo():
    caretaker = CalculatorCaretaker()
    history = ["add", "multiply"]

    caretaker.save_state(["add"])

    result = caretaker.undo(history)

    assert result == ["add"]


def test_redo():
    caretaker = CalculatorCaretaker()

    caretaker.save_state(["add"])

    previous = caretaker.undo(["add", "multiply"])
    result = caretaker.redo(previous)

    assert result == ["add", "multiply"]


def test_undo_empty_stack():
    caretaker = CalculatorCaretaker()

    assert caretaker.undo([]) is None


def test_redo_empty_stack():
    caretaker = CalculatorCaretaker()

    assert caretaker.redo([]) is None


def test_new_calculation_clears_redo():
    caretaker = CalculatorCaretaker()

    caretaker.save_state([])
    caretaker.undo(["add"])

    caretaker.save_state(["multiply"])

    assert caretaker.redo(["multiply", "subtract"]) is None


def test_multiple_undo_redo():
    caretaker = CalculatorCaretaker()

    caretaker.save_state([])
    caretaker.save_state(["add"])

    history = caretaker.undo(["add", "multiply"])
    assert history == ["add"]

    history = caretaker.undo(history)
    assert history == []

    history = caretaker.redo(history)
    assert history == ["add"]

    history = caretaker.redo(history)
    assert history == ["add", "multiply"]
