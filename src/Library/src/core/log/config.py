"""Logging configuration."""

import logging
import sys
import os
import json
from pathlib import Path

from loguru import logger

from src.core.config import settings

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Intercept log messages and pass them to loguru.

        Args:
            record: Log record
        """
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class JsonSink:
    """Custom sink that writes JSON formatted logs to a file."""

    def __init__(self, file_path):
        self.file_path = file_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def write(self, message):
        record = message.record
        log_entry = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "name": record["name"],
            "function": record["function"],
            "line": record["line"],
            "service": "library",  # Hardcode service name
            "environment": settings.APP_ENV,
        }

        # Add exception info if present
        if record["exception"]:
            log_entry["exception"] = str(record["exception"])

        # Write to file
        with open(self.file_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")


def setup_logging() -> None:
    """Configure logging with loguru."""
    # Remove default handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.LOG_LEVEL)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(
        handlers=[
            # Console handler
            {
                "sink": sys.stdout,
                "level": settings.LOG_LEVEL,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            },
            # JSON file handler for Filebeat
            {
                "sink": JsonSink("logs/library.log"),
                "level": settings.LOG_LEVEL,
            },
        ]
    )

    # Add specific loggers
    logger.info("Logging is configured.")
