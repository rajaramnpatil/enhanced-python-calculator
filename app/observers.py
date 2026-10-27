
from abc import ABC, abstractmethod


class CalculatorObserver(ABC):
    """Base class for calculator observers."""

    @abstractmethod
    def update(self, event, calculation=None):
        """Handle a calculator event."""


class CalculatorSubject:
    """Manages observers and sends notifications."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event, calculation=None):
        for observer in self._observers:
            observer.update(event, calculation)

class AutoSaveObserver(CalculatorObserver):
    """Automatically saves history when it changes."""

    def __init__(self, history_manager, history_provider):
        self.history_manager = history_manager
        self.history_provider = history_provider

    def update(self, event, calculation=None):
        if event in ("calculation", "undo", "redo", "clear"):
            self.history_manager.save(
                self.history_provider()
            )
