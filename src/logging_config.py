"""Logging configuration utilities."""

import logging

from src.settings import settings


def setup_logging(level: int | str | None = None) -> None:
    """Set up and configure the root logger with a formatted handler.

    Clears any existing handlers and initializes the root logger with a
    StreamHandler using a standard format. Uses the provided log level or
    falls back to the level from settings if not specified.

    Args:
        level: Optional logging level (int, str, or None). If None, uses
               the log level from settings.
    """
    # Clear existing handlers to avoid duplicate logs if setup is called multiple times
    root = logging.getLogger()
    if root.handlers:
        root.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Use log level from environment variables if not explicitly provided.
    if level is None:
        level = settings.log_level
    root.setLevel(level)
    root.addHandler(handler)
