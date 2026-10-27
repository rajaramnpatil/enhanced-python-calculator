
import math

import pandas as pd

from app.calculation import Calculation
from app.exceptions import HistoryError


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
        """Save calculation history to CSV safely."""
        try:
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

        except (OSError, ValueError, UnicodeError) as exc:
            raise HistoryError(
                f"Unable to save calculation history: {exc}"
            ) from exc

    def load(self):
        """Load and validate calculation history from CSV."""
        path = self.config.history_file_path

        if not path.exists():
            return []

        try:
            df = pd.read_csv(
                path,
                encoding=self.config.default_encoding,
            )

            if list(df.columns) != self.COLUMNS:
                raise HistoryError(
                    "Invalid history CSV format."
                )

            history = []

            for row in df.itertuples(index=False):
                operand1 = float(row.operand1)
                operand2 = float(row.operand2)

                if not all(
                    math.isfinite(value)
                    for value in (operand1, operand2)
                ):
                    raise HistoryError(
                        "History contains invalid numeric values."
                    )

                calculation = Calculation(
                    operation=row.operation,
                    operand1=operand1,
                    operand2=operand2,
                )

                # Restore the original timestamp.
                calculation.timestamp = pd.Timestamp(
                    row.timestamp
                ).to_pydatetime()

                # Verify the stored result matches the calculation.
                stored_result = float(row.result)

                if not math.isfinite(stored_result):
                    raise HistoryError(
                        "History contains an invalid result."
                    )

                if not math.isclose(
                    calculation.result,
                    stored_result,
                    rel_tol=1e-9,
                    abs_tol=1e-9,
                ):
                    raise HistoryError(
                        "History contains an incorrect result."
                    )

                history.append(calculation)

            return history

        except HistoryError:
            raise

        except (
            OSError,
            ValueError,
            TypeError,
            UnicodeError,
            OverflowError,
            pd.errors.ParserError,
            pd.errors.EmptyDataError,
        ) as exc:
            raise HistoryError(
                f"Unable to load calculation history: {exc}"
            ) from exc
