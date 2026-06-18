"""Tests for settings module."""

import pytest
from pydantic import ValidationError

from src.settings import AppSettings, LogLevel


def test_default_settings() -> None:
    """Default settings are applied when no environment variables are set."""
    s = AppSettings()
    assert s.log_level == LogLevel.INFO


def test_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables override default settings."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    s = AppSettings()
    assert s.log_level == LogLevel.DEBUG


def test_strips_whitespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Whitespace is stripped from string settings."""
    monkeypatch.setenv("LOG_LEVEL", "  WARNING  ")
    s = AppSettings()
    assert s.log_level == LogLevel.WARNING


def test_empty_string_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """An empty string value raises a validation error."""
    monkeypatch.setenv("LOG_LEVEL", "   ")
    with pytest.raises(ValidationError):
        AppSettings()


def test_str_representation() -> None:
    """__str__ returns a formatted settings summary."""
    s = AppSettings()
    result = str(s)
    assert "Application Settings:" in result
    assert "log_level" in result
