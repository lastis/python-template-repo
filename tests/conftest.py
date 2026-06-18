"""Test configuration and fixtures.

Sets environment variable defaults before any src module is imported.
This ensures AppSettings() sees clean values in unit tests, overriding
anything injected into the OS environment by the task runner loading .env.
"""

import os

# These override .env file values because os.environ takes precedence over
# pydantic-settings env_file. Set before any src imports so module-level
# settings objects are also initialised with the right values.
os.environ.setdefault("LOG_LEVEL", "INFO")
