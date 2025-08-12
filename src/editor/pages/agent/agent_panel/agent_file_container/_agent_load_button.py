from editor.components import FileLoaderOverlay, LoadButton
from agent.config import AGENT_SAVE_FOLDER_PATH


class _LoadAgentOverlay(FileLoaderOverlay):

    def __init__(self):
        super().__init__(AGENT_SAVE_FOLDER_PATH, "agent")

    def _load(self):
        from agent_loader import agent_loader
        from app_manager import app_manager

        super()._load()
        agent_loader.load_agent(self._get_file_path())
        app_manager.editor_app.restart_all_pages()


class AgentLoadButton(LoadButton):
    def _on_click(self, event):
        _LoadAgentOverlay()
