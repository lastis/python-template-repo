"""Tests for logging_config module."""

import logging

from src.logging_config import setup_logging


def test_setup_logging_adds_handler() -> None:
    """setup_logging should add exactly one handler to the root logger."""
    setup_logging()
    root = logging.getLogger()
    assert len(root.handlers) == 1


def test_setup_logging_sets_level() -> None:
    """setup_logging should set the root logger level to the provided value."""
    setup_logging(level=logging.DEBUG)
    root = logging.getLogger()
    assert root.level == logging.DEBUG


def test_setup_logging_replaces_existing_handlers() -> None:
    """Calling setup_logging twice should not accumulate handlers."""
    setup_logging()
    setup_logging()
    root = logging.getLogger()
    assert len(root.handlers) == 1
