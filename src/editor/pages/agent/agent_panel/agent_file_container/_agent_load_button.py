from editor.components import FileLoaderOverlay, LoadButton
from agent.config import AGENT_SAVE_FOLDER_PATH
from editor.components.overlay.file_loader_overlay.file_loader_overlay_spawner import (
    FileLoaderOverlaySpawner,
)


class _AgentLoaderOverlay(FileLoaderOverlay):
    def _load(self):
        from agent_loader import agent_loader
        from app_manager import app_manager

        super()._load()
        agent_loader.load_agent(self._get_file_path())
        app_manager.editor_app.restart_all_pages()


class AgentLoadButton(LoadButton):
    def _on_click(self, event):
        FileLoaderOverlaySpawner(AGENT_SAVE_FOLDER_PATH, "agent", _AgentLoaderOverlay)
