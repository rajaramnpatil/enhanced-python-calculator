
import logging

from app.observers import CalculatorObserver


def setup_logger(config):
    """Configure application logging."""

    config.log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("enhanced_calculator")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_path = config.log_file_path.resolve()

    # Avoid adding duplicate handlers.
    for handler in logger.handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and handler.baseFilename == str(log_path)
        ):
            return logger

    handler = logging.FileHandler(
        log_path,
        encoding=config.default_encoding
    )

    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
    )

    logger.addHandler(handler)
    return logger


class LoggingObserver(CalculatorObserver):
    """Records calculator events in a log file."""

    def __init__(self, logger):
        self.logger = logger

    def update(self, event, calculation=None):
        if event == "calculation" and calculation is not None:
            self.logger.info(
                "%s(%s, %s) = %s",
                calculation.operation,
                calculation.operand1,
                calculation.operand2,
                calculation.result,
            )
        elif event == "error":
            self.logger.error("%s", calculation)
        else:
            self.logger.info("Calculator event: %s", event)
