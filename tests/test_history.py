
import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
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
