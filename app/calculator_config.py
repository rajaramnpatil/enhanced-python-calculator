
import math
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from app.exceptions import ValidationError


load_dotenv()


@dataclass
class CalculatorConfig:
    """This class manages calculator configuration settings."""

    log_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("CALCULATOR_LOG_DIR", "logs")
        )
    )

    history_dir: Path = field(
        default_factory=lambda: Path(
            os.getenv("CALCULATOR_HISTORY_DIR", "history")
        )
    )

    log_file: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_LOG_FILE", "calculator.log"
        )
    )

    history_file: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_HISTORY_FILE", "history.csv"
        )
    )

    max_history_size: int = field(
        default_factory=lambda: int(
            os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "100")
        )
    )

    auto_save: bool = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_AUTO_SAVE", "true"
        ).lower() == "true"
    )

    precision: int = field(
        default_factory=lambda: int(
            os.getenv("CALCULATOR_PRECISION", "2")
        )
    )

    max_input_value: float = field(
        default_factory=lambda: float(
            os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000")
        )
    )

    default_encoding: str = field(
        default_factory=lambda: os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )
    )

    def __post_init__(self):
        """Convert directory values to Path objects and validate."""

        self.log_dir = Path(self.log_dir)
        self.history_dir = Path(self.history_dir)

        self.validate()

    def validate(self):
        """Validate configuration values."""

        if self.max_history_size <= 0:
            raise ValidationError(
                "Maximum history size must be positive."
            )

        if self.precision < 0:
            raise ValidationError(
                "Precision cannot be negative."
            )

        if (
            not math.isfinite(self.max_input_value)
            or self.max_input_value <= 0
        ):
            raise ValidationError(
                "Maximum input value must be finite and positive."
            )

        if not self.default_encoding:
            raise ValidationError(
                "Default encoding cannot be empty."
            )

    @property
    def log_file_path(self):
        return self.log_dir / self.log_file

    @property
    def history_file_path(self):
        return self.history_dir / self.history_file
