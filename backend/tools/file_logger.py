import logging
from pathlib import Path


class Logger:
    _initialized = False
    _logger = None

    @staticmethod
    def initialize(
        log_file: str = "logs/app.log",
        level=logging.DEBUG,
    ):
        """
        Initializes the logger once.
        """

        if Logger._initialized:
            return

        # Create logs directory if it doesn't exist
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("CLI_APP")
        logger.setLevel(level)

        # Prevent duplicate handlers
        logger.handlers.clear()

        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        Logger._logger = logger
        Logger._initialized = True

    @staticmethod
    def debug(message: str):
        Logger._logger.debug(message)

    @staticmethod
    def info(message: str):
        Logger._logger.info(message)

    @staticmethod
    def warning(message: str):
        Logger._logger.warning(message)

    @staticmethod
    def error(message: str):
        Logger._logger.error(message)

    @staticmethod
    def critical(message: str):
        Logger._logger.critical(message)