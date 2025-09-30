import customtkinter as ctk
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer
from ._train_container import TrainContainer
from ._train_logs_panel import TrainLogsPanel
from training_state_manager import training_state_manager


class AgentPanel(ctk.CTkFrame):
    COLLECT_STEPS_PER_ITERATION = 150
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", width=128)

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=(0, 8), fill="x")

        train_container = TrainContainer(self)
        train_container.pack(padx=2, pady=(2, 24))

        self.episodes_label = ctk.CTkLabel(self)
        self.episodes_label.pack(pady=0, anchor="w")
        self.episodes_slider = ctk.CTkSlider(
            self,
            from_=self.COLLECT_STEPS_PER_ITERATION,
            to=20000,
            width=self.COLLECT_STEPS_PER_ITERATION,
            height=20,
        )
        self.episodes_slider.pack(pady=(0, 24), fill="x")
        self._set_amount_of_episodes(self.COLLECT_STEPS_PER_ITERATION * 5)

        self.episodes_slider.configure(command=self._on_episode_slide)

        train_logs_panel = TrainLogsPanel(self)
        train_logs_panel.pack(padx=2, pady=(0, 10), fill="x")
        training_state_manager.set_train_logs_panel(train_logs_panel)

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    def _on_episode_slide(self, value):
        rounded_value = (
            round(value / self.COLLECT_STEPS_PER_ITERATION)
            * self.COLLECT_STEPS_PER_ITERATION
        )
        self._set_amount_of_episodes(rounded_value)

    def _set_amount_of_episodes(self, value):
        self.episodes_slider.set(value)
        self.episodes_label.configure(text=f"Episodes: {value}")
        training_state_manager.amount_of_episodes = value
