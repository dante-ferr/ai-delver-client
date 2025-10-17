import sys
import json
from pathlib import Path
from typing import Any


class Config:
    """A class to hold and provide access to configuration settings from a JSON file."""

    def __init__(self, config_path: str = "src/config.json"):
        self._config_path = Path(config_path)
        self._data = self._load_config()

        self.PROJECT_ROOT = self.get_project_root()
        self.ASSETS_PATH = self.PROJECT_ROOT / "assets"

    def _load_config(self) -> dict:
        with open(self._config_path, "r") as f:
            return json.load(f)

    def __getattr__(self, name: str) -> Any:
        # Converts Python's UPPER_SNAKE_CASE to json's snake_case for lookup
        key = name.lower()
        if key in self._data:
            return self._data[key]
        raise AttributeError(
            f"Configuration '{self._config_path}' has no setting '{key}'"
        )

    def get_project_root(self) -> Path:
        """
        Determines the project's root directory, whether running from source
        or as a frozen executable (e.g., from PyInstaller).
        """
        if getattr(sys, "frozen", False):
            # If it is frozen, the root is the directory containing the executable.
            # sys.executable gives the path to MyGame.exe.
            application_path = Path(sys.executable)
            return application_path.parent
        else:
            # If it's not frozen, we are running from source code.
            # The project root is three levels up from this config file's location.
            # (src/ -> ai-delver-client/ -> ai-delver/)
            return Path(__file__).resolve().parent.parent.parent


# A single, global instance for easy access throughout the application.
config = Config()
