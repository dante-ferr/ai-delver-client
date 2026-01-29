import customtkinter as ctk
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer
from ._train_container import TrainContainer
from ._train_logs_panel import TrainLogsPanel
from state_managers import training_state_manager
from app.components import RangeSliderInput

class AgentPanel(ctk.CTkFrame):
    EPISODES_BATCH = 20
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", width=128)

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=(0, 8), fill="x")

        train_container = TrainContainer(self)
        train_container.pack(padx=2, pady=(2, 24))

        init_val = 10
        self.training_cycles_input = RangeSliderInput(
            self,
            label_text="Training Cycles:",
            min_val=1,
            max_val=100,
            init_val=init_val,
            step=1,
            on_update=self._set_training_cycles,
        )
        training_state_manager.amount_of_cycles = init_val
        self.training_cycles_input.pack(pady=(0, 24), fill="x")

        init_val = 50
        self.episodes_per_cycle_input = RangeSliderInput(
            self,
            label_text="Episodes per Cycle:",
            min_val=10,
            max_val=200,
            init_val=50,
            step=10,
            on_update=self._set_episodes_per_cycle,
        )
        training_state_manager.episodes_per_cycle = init_val
        self.episodes_per_cycle_input.pack(pady=(0, 24), fill="x")

        self.episodes_label = ctk.CTkLabel(self, text=f"{self.EPISODES_BATCH} episodes")
        self.episodes_label.pack(anchor="w")

        # Set initial amount of episodes immediately
        self._set_amount_of_episodes()

        train_logs_panel = TrainLogsPanel(self)
        train_logs_panel.pack(padx=2, pady=(0, 10), fill="x")
        training_state_manager.set_train_logs_panel(train_logs_panel)

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    def _set_training_cycles(self, value):
        training_state_manager.amount_of_cycles = value
        self._set_amount_of_episodes()

    def _set_episodes_per_cycle(self, value):
        training_state_manager.episodes_per_cycle = value
        self._set_amount_of_episodes()

    def _set_amount_of_episodes(self):
        episodes = int(
            self.training_cycles_input.get() * self.episodes_per_cycle_input.get()
        )
        self.episodes_label.configure(text=f"{episodes} episodes")
