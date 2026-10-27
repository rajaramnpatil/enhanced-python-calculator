
import pandas as pd
import pytest

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.exceptions import HistoryError
from app.history import HistoryManager
from app.observers import AutoSaveObserver


def test_save_and_load_history(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path
    )
    manager = HistoryManager(config)

    history = [
        Calculation("add", 10, 5),
        Calculation("multiply", 2, 3),
    ]

    manager.save(history)

    assert config.history_file_path.exists()

    loaded = manager.load()

    assert len(loaded) == 2
    assert loaded[0].result == 15
    assert loaded[1].result == 6


def test_save_empty_history(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path
    )
    manager = HistoryManager(config)

    manager.save([])

    df = pd.read_csv(config.history_file_path)

    assert df.empty
    assert list(df.columns) == HistoryManager.COLUMNS


def test_load_missing_file(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path
    )
    manager = HistoryManager(config)

    assert manager.load() == []


def test_autosave_observer(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path
    )
    manager = HistoryManager(config)

    history = [Calculation("add", 10, 5)]

    observer = AutoSaveObserver(
        manager,
        lambda: history,
    )

    observer.update("calculation", history[0])

    assert config.history_file_path.exists()


def test_autosave_ignores_other_events(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path
    )
    manager = HistoryManager(config)

    observer = AutoSaveObserver(
        manager,
        lambda: [],
    )

    observer.update("help")

    assert not config.history_file_path.exists()


def make_history_manager(tmp_path):
    config = CalculatorConfig(
        history_dir=tmp_path / "history",
        log_dir=tmp_path / "logs",
        auto_save=False,
    )
    return HistoryManager(config)


def test_load_invalid_columns(tmp_path):
    manager = make_history_manager(tmp_path)

    manager.config.history_dir.mkdir(
        parents=True, exist_ok=True
    )

    manager.config.history_file_path.write_text(
        "wrong,column\n1,2\n"
    )

    with pytest.raises(HistoryError):
        manager.load()


def test_load_empty_csv(tmp_path):
    manager = make_history_manager(tmp_path)

    manager.config.history_dir.mkdir(
        parents=True, exist_ok=True
    )

    manager.config.history_file_path.write_text("")

    with pytest.raises(HistoryError):
        manager.load()


def test_load_invalid_numeric_value(tmp_path):
    manager = make_history_manager(tmp_path)

    manager.config.history_dir.mkdir(
        parents=True, exist_ok=True
    )

    manager.config.history_file_path.write_text(
        "operation,operand1,operand2,result,timestamp\n"
        "add,invalid,2,3,2026-10-27T10:00:00\n"
    )

    with pytest.raises(HistoryError):
        manager.load()


def test_load_incorrect_result(tmp_path):
    manager = make_history_manager(tmp_path)

    manager.config.history_dir.mkdir(
        parents=True, exist_ok=True
    )

    manager.config.history_file_path.write_text(
        "operation,operand1,operand2,result,timestamp\n"
        "add,1,2,999,2026-10-27T10:00:00\n"
    )

    with pytest.raises(HistoryError):
        manager.load()


def test_save_file_error(tmp_path, monkeypatch):
    manager = make_history_manager(tmp_path)

    def fail_save(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr(
        "pandas.DataFrame.to_csv",
        fail_save,
    )

    with pytest.raises(HistoryError):
        manager.save([])


