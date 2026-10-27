
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CalculatorMemento:
    """This class stores a snapshot of calculator history."""

    history: tuple[Any, ...]


class CalculatorCaretaker:
    """This class manages saved states for undo and redo."""

    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, history):
        """Save current history before making a change."""
        memento = CalculatorMemento(tuple(history))
        self.undo_stack.append(memento)

        # New calculations invalidate redo history.
        self.redo_stack.clear()

    def undo(self, current_history):
        """Restore the previous calculator state."""
        if not self.undo_stack:
            return None

        self.redo_stack.append(
            CalculatorMemento(tuple(current_history))
        )

        previous = self.undo_stack.pop()
        return list(previous.history)

    def redo(self, current_history):
        """Restore the most recently undone state."""
        if not self.redo_stack:
            return None

        self.undo_stack.append(
            CalculatorMemento(tuple(current_history))
        )

        next_state = self.redo_stack.pop()
        return list(next_state.history)
