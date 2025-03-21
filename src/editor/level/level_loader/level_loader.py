from ..level import SAVE_FOLDER_PATH
import dill
from ._level_factory import LevelFactory
from pathlib import Path

DEFAULT_LEVEL_NAME = "My custom level"
DEFAULT_FILE_PATH = SAVE_FOLDER_PATH / f"{DEFAULT_LEVEL_NAME}.dill"


class LevelLoader:
    def __init__(self):
        self.factory = LevelFactory()
        self._create_new_level()

    def load_level(self, path: Path):
        if path.is_file():
            try:
                with open(path, "rb") as file:
                    self.level = dill.load(file)
                    self._restart_level_editor()
            except Exception as e:
                print(f"Error loading instance: {e}. Creating a new one.")
                self._create_new_level()
        else:
            self._create_new_level()

    def _create_new_level(self):
        self.level = self.factory.create_level()

    def _restart_level_editor(self):
        from ...editor import app as editor_app

        editor_app.restart_level_editor()


level_loader = LevelLoader()
