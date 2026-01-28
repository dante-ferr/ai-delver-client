import customtkinter as ctk
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer
from ._train_container import TrainContainer
from ._train_logs_panel import TrainLogsPanel
from training_state_manager import training_state_manager


class AgentPanel(ctk.CTkFrame):
    EPISODES_BATCH = 20
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", width=128)

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=(0, 8), fill="x")

        train_container = TrainContainer(self)
        train_container.pack(padx=2, pady=(2, 24))

        self.iterations_label = ctk.CTkLabel(self)
        self.iterations_label.pack(pady=0, anchor="w")
        self.episodes_batch_slider = ctk.CTkSlider(
            self,
            from_=1,
            to=250,
            height=20,
        )
        self.episodes_batch_slider.pack(pady=(0, 24), fill="x")
        self._set_episode_batches(20)

        self.episodes_batch_slider.configure(command=self._on_iteration_slide)

        train_logs_panel = TrainLogsPanel(self)
        train_logs_panel.pack(padx=2, pady=(0, 10), fill="x")
        training_state_manager.set_train_logs_panel(train_logs_panel)

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    def _on_iteration_slide(self, value):
        self._set_episode_batches(int(value))

    def _set_episode_batches(self, value):
        self.episodes_batch_slider.set(value)
        episodes = value * self.EPISODES_BATCH
        self.iterations_label.configure(text=f"{episodes} episodes")
        training_state_manager.amount_of_episodes = episodes
