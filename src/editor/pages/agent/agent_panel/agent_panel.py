import customtkinter as ctk
import asyncio
from editor.utils import verify_level_issues
from client_requests import send_training_request
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer


class AgentPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=0, fill="x")

        train_button = ctk.CTkButton(
            self, text="Train", command=lambda: asyncio.run(self._train())
        )
        train_button.pack(pady=8)

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    async def _train(self):
        if not verify_level_issues():
            await send_training_request()
