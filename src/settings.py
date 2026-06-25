"""Application settings using Pydantic Settings.

This module provides a centralized place to define and access application settings.
The settings are automatically loaded from environment variables or .env files.
"""

from enum import StrEnum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    """Enumeration of valid log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables.

    Environment variables are case-insensitive and are loaded from .env file and the system
    environment. All values are automatically stripped of whitespace and must be non-empty.

    Sensitive fields use SecretStr to prevent accidental logging. Use `.get_secret_value()`
    to access the actual value when needed.
    """

    # Variables that can be populated from environment variables or .env file:
    log_level: LogLevel = LogLevel.INFO

    # Ignore extra environment variables that aren't part of this settings model
    # (e.g., UV_INDEX_AZURE_PASSWORD used for package installation)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Strip and validate all string fields to ensure they are non-empty.
    # Use mode="before" to process raw input and avoid issues with SecretStr
    @field_validator("*", mode="before")
    @classmethod
    def check_non_empty(cls, v: object) -> object:
        """Strip whitespace, surrounding quotes, and ensure the value is not empty.

        Surrounding quotes are stripped to handle the case where environment variables
        are loaded from a .env file by tools that do not perform dotenv-style quote
        stripping (e.g. VS Code terminal integration, PowerShell dotenv loaders).
        A proper dotenv parser (like python-dotenv) would already strip these quotes,
        but when the OS environment variable is set directly with literal quote
        characters, they must be stripped here.
        """
        if isinstance(v, str):
            stripped = v.strip()
            # Strip matching surrounding double or single quotes
            if len(stripped) >= 2 and (
                (stripped[0] == '"' and stripped[-1] == '"')
                or (stripped[0] == "'" and stripped[-1] == "'")
            ):
                stripped = stripped[1:-1]
            if not stripped:
                raise ValueError("Value must be a non-empty string")
            return stripped
        return v

    def __str__(self) -> str:
        """Return a formatted string representation of the settings."""
        settings_dict = self.model_dump()
        max_key_len = max(len(key) for key in settings_dict)
        lines = ["Application Settings:"]
        for key, value in settings_dict.items():
            padded_key = key.ljust(max_key_len)
            lines.append(f"    {padded_key} : {value}")
        return "\n".join(lines)


# Define the settings object at the module level so
# it can be imported and used throughout the application.
settings = AppSettings()
"""
Settings object that makes environment variables available throughout the application with
type safety and validation.
"""
