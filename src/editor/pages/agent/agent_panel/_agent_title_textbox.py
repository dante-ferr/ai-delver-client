from editor.components import TitleTextbox
from agent_loader import agent_loader


class AgentTitleTextbox(TitleTextbox):
    def __init__(self, parent):
        super().__init__(parent, agent_loader.agent.name)

    def _update_name(self, event=None):
        agent_loader.agent.name = self._get_input()
