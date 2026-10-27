
from unittest.mock import Mock

from app.observers import CalculatorSubject
from app.logger import LoggingObserver, setup_logger
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation


def test_attach_and_notify():
    subject = CalculatorSubject()
    observer = Mock()

    subject.attach(observer)
    subject.notify("clear")

    observer.update.assert_called_once_with("clear", None)


def test_detach_observer():
    subject = CalculatorSubject()
    observer = Mock()

    subject.attach(observer)
    subject.detach(observer)
    subject.notify("clear")

    observer.update.assert_not_called()


def test_duplicate_observer():
    subject = CalculatorSubject()
    observer = Mock()

    subject.attach(observer)
    subject.attach(observer)
    subject.notify("clear")

    observer.update.assert_called_once()


def test_logging_calculation(tmp_path):
    config = CalculatorConfig(log_dir=tmp_path)
    logger = setup_logger(config)
    observer = LoggingObserver(logger)

    calculation = Calculation("add", 10, 5)
    observer.update("calculation", calculation)

    for handler in logger.handlers:
        handler.flush()

    content = config.log_file_path.read_text()

    assert "add(10, 5) = 15" in content


def test_logging_error(tmp_path):
    config = CalculatorConfig(log_dir=tmp_path)
    logger = setup_logger(config)
    observer = LoggingObserver(logger)

    observer.update("error", "Division by zero")

    for handler in logger.handlers:
        handler.flush()

    content = config.log_file_path.read_text()

    assert "ERROR" in content
    assert "Division by zero" in content


def test_logging_history_event(tmp_path):
    config = CalculatorConfig(log_dir=tmp_path)
    logger = setup_logger(config)
    observer = LoggingObserver(logger)

    observer.update("undo")

    for handler in logger.handlers:
        handler.flush()

    content = config.log_file_path.read_text()

    assert "Calculator event: undo" in content
