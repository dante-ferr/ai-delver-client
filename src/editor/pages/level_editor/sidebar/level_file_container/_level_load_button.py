from editor.components import FileLoaderOverlay, LoadButton
from level.config import LEVEL_SAVE_FOLDER_PATH


class _LoadLevelOverlay(FileLoaderOverlay):

    def __init__(self):
        super().__init__(LEVEL_SAVE_FOLDER_PATH, "level")

    def _load(self):
        from level_loader import level_loader
        from app_manager import app_manager

        super()._load()
        level_loader.load_level(self._get_file_path())
        app_manager.editor_app.restart_all_pages()


class LevelLoadButton(LoadButton):
    def _on_click(self, event):
        _LoadLevelOverlay()
