import customtkinter as ctk
from ._train_logs_panel import TrainLogsPanel
from state_managers import training_state_manager
from app.components import RangeSliderInput
from ._train_buttons_container import TrainButtonsContainer
from app.components import SortableList
from src.config import config

class TrainPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    MAX_ENV_BATCHES_PER_CYCLE = 20

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", width=128)

        train_container = TrainButtonsContainer(self)
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
        self.training_cycles_input.pack(pady=(0, 16), fill="x")

        init_val = 50
        self.episodes_per_cycle_input = RangeSliderInput(
            self,
            label_text="Episodes per Cycle:",
            on_update=self._set_episodes_per_cycle,
        )
        training_state_manager.episodes_per_cycle = init_val
        self.episodes_per_cycle_input.pack(pady=(0, 24), fill="x")

        self.episodes_label = ctk.CTkLabel(
            self, text=f"", font=ctk.CTkFont(size=config.STYLE.FONT.STANDARD_SIZE)
        )
        self.episodes_label.pack(anchor="w")

        self._set_amount_of_episodes()

        sortable_list = SortableList(self, height=300, remove_box_button=True)
        sortable_list.pack(pady=(0, 24), fill="x")
        sortable_list.add_box("aaaaaaaaaaaaaaa")
        sortable_list.add_box("bbbbbbbbbbbbbb")
        sortable_list.add_box("ccccccccccccccccccc")
        sortable_list.add_box("ddddddddddddd")
        sortable_list.add_box("eeeeeeeeeeeeeeeee")
        sortable_list.add_box("ffffffffffff")
        sortable_list.add_box("gggggggggggggggg")
        sortable_list.add_box("hhhhhhhhhhhhhhhhhhh")
        sortable_list.add_box("aaaaaaaaaaaaaaa")
        sortable_list.add_box("bbbbbbbbbbbbbb")
        sortable_list.add_box("ccccccccccccccccccc")
        sortable_list.add_box("ddddddddddddd")
        sortable_list.add_box("eeeeeeeeeeeeeeeee")
        sortable_list.add_box("ffffffffffff")
        sortable_list.add_box("gggggggggggggggg")
        sortable_list.add_box("hhhhhhhhhhhhhhhhhhh")
        sortable_list.add_box("aaaaaaaaaaaaaaa")
        sortable_list.add_box("bbbbbbbbbbbbbb")
        sortable_list.add_box("ccccccccccccccccccc")
        sortable_list.add_box("ddddddddddddd")
        sortable_list.add_box("eeeeeeeeeeeeeeeee")
        sortable_list.add_box("ffffffffffff")
        sortable_list.add_box("gggggggggggggggg")
        sortable_list.add_box("hhhhhhhhhhhhhhhhhhh")

        train_logs_panel = TrainLogsPanel(self)
        train_logs_panel.pack(padx=2, pady=(0, 10), fill="x")
        training_state_manager.set_train_logs_panel(train_logs_panel)

        training_state_manager.add_callback(
            "env_batch_size", self._on_env_batch_size_update
        )

    def _on_env_batch_size_update(self, value):
        self.episodes_per_cycle_input.configure(
            min_val=value, step=value, max_val=self.MAX_ENV_BATCHES_PER_CYCLE * value
        )
        self.episodes_per_cycle_input.set_value(value)

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
