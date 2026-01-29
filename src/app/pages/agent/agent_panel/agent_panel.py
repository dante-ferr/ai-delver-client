import customtkinter as ctk
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer
from .train_panel import TrainPanel
from ._server_connection_panel import ServerConnectionPanel
from state_managers import training_state_manager
from app.components import LoadingLogsPanel

class AgentPanel(ctk.CTkFrame):
    EPISODES_BATCH = 20
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", width=128)

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=(0, 8), fill="x")

        self.train_panel_frame = ctk.CTkFrame(self)
        self.train_panel_frame.pack(fill="both")

        self.train_panel = TrainPanel(self.train_panel_frame)
        self.server_connection_panel = ServerConnectionPanel(self.train_panel_frame)

        self.server_loading_logs_panel = LoadingLogsPanel(self.train_panel_frame)
        self.server_loading_logs_panel.pack(pady=10, fill="x")

        training_state_manager.add_callback(
            "connected_to_server", self._on_connected_to_server_status_change
        )
        self._on_connected_to_server_status_change(
            training_state_manager.get_value("connected_to_server")
        )

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    def _on_connected_to_server_status_change(self, connected_to_server: str):
        if connected_to_server == "yes":
            self.server_connection_panel.pack_forget()
            self.train_panel.pack(padx=2, pady=(0, 10), fill="x")

            self.server_loading_logs_panel.remove_log("loading_server")

        elif connected_to_server == "no":
            self.train_panel.pack_forget()
            self.server_connection_panel.pack(padx=2, pady=(0, 10), fill="x")

            self.server_loading_logs_panel.remove_log("loading_server")

        elif connected_to_server == "loading":
            self.train_panel.pack_forget()
            self.server_connection_panel.pack_forget()

            self.server_loading_logs_panel.show_log(
                "loading_server", "Loading server..."
            )
