import customtkinter as ctk
from app.components import RangeSliderInput
from typing import Callable
from state_managers import training_state_manager


class EpisodesSettingPanel(ctk.CTkFrame):
    MAX_ENV_BATCHES_PER_CYCLE = 20

    def __init__(self, master, on_amount_of_episodes_change: Callable):
        super().__init__(master, fg_color="transparent")

        self.on_amount_of_episodes_change = on_amount_of_episodes_change

        init_val = 10
        self.training_cycles_input = RangeSliderInput(
            self,
            label_text="Training Cycles:",
            min_val=1,
            max_val=100,
            init_val=init_val,
            step=1,
            on_update=self._set_training_cycles,
            fg_color="transparent",
        )
        self.training_cycles_input.pack(pady=(0, 16), fill="x")
        training_state_manager.amount_of_cycles = init_val

        init_val = 50
        self.episodes_per_cycle_input = RangeSliderInput(
            self,
            label_text="Episodes per Cycle:",
            on_update=self._set_episodes_per_cycle,
            fg_color="transparent",
        )
        self.episodes_per_cycle_input.pack(pady=0, fill="x")
        training_state_manager.episodes_per_cycle = init_val

        training_state_manager.add_callback(
            "env_batch_size", self._on_env_batch_size_update
        )

    def _set_training_cycles(self, value):
        training_state_manager.amount_of_cycles = value
        self.on_amount_of_episodes_change()

    def _set_episodes_per_cycle(self, value):
        training_state_manager.episodes_per_cycle = value
        self.on_amount_of_episodes_change()

    def _on_env_batch_size_update(self, value):
        self.episodes_per_cycle_input.configure(
            min_val=value, step=value, max_val=self.MAX_ENV_BATCHES_PER_CYCLE * value
        )
        self.episodes_per_cycle_input.set_value(value)
