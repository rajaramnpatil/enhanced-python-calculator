
import pandas as pd

from app.calculation import Calculation


class HistoryManager:
    """Save and load calculator history using pandas."""

    COLUMNS = [
        "operation",
        "operand1",
        "operand2",
        "result",
        "timestamp",
    ]

    def __init__(self, config):
        self.config = config

    def save(self, history):
        self.config.history_dir.mkdir(
            parents=True, exist_ok=True
        )

        rows = [
            {
                "operation": item.operation,
                "operand1": item.operand1,
                "operand2": item.operand2,
                "result": item.result,
                "timestamp": item.timestamp.isoformat(),
            }
            for item in history
        ]

        df = pd.DataFrame(rows, columns=self.COLUMNS)

        df.to_csv(
            self.config.history_file_path,
            index=False,
            encoding=self.config.default_encoding,
        )

    def load(self):
        path = self.config.history_file_path

        if not path.exists():
            return []

        df = pd.read_csv(
            path,
            encoding=self.config.default_encoding,
        )

        if list(df.columns) != self.COLUMNS:
            raise ValueError("Invalid history CSV format.")

        history = []

        for row in df.itertuples(index=False):
            calculation = Calculation(
                operation=row.operation,
                operand1=float(row.operand1),
                operand2=float(row.operand2),
            )

            # Restore the original timestamp.
            calculation.timestamp = pd.Timestamp(
                row.timestamp
            ).to_pydatetime()

            # The result is recalculated by Calculation.
            history.append(calculation)

        return history
