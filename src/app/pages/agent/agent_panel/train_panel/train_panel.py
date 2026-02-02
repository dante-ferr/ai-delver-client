import customtkinter as ctk
from ._train_logs_panel import TrainLogsPanel
from ._train_buttons_container import TrainButtonsContainer
from src.config import config
from .level_selector import LevelSelector
from ._episodes_setting_panel import EpisodesSettingPanel

class TrainPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", width=128)

        train_buttons_container = TrainButtonsContainer(self)
        train_buttons_container.pack(padx=2, pady=(0, config.STYLE.SECTION_SPACING))

        self.episodes_setting_panel = EpisodesSettingPanel(
            self, on_amount_of_episodes_change=self._set_amount_of_episodes
        )
        self.episodes_setting_panel.pack(
            pady=(0, config.STYLE.SECTION_SPACING), fill="x"
        )

        self.cycles_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=config.STYLE.FONT.STANDARD_SIZE)
        )
        self.cycles_label.pack(anchor="w", pady=0)

        self.episodes_label = ctk.CTkLabel(
            self, text=f"", font=ctk.CTkFont(size=config.STYLE.FONT.STANDARD_SIZE)
        )
        self.episodes_label.pack(anchor="w", pady=(0, config.STYLE.SECTION_SPACING))

        self.level_selector = LevelSelector(
            self, on_amount_of_episodes_change=self._set_amount_of_episodes, height=240
        )
        self.level_selector.pack(pady=(0, config.STYLE.SECTION_SPACING), fill="x")

        train_logs_panel = TrainLogsPanel(self)
        train_logs_panel.pack(padx=2, pady=(0, config.STYLE.SECTION_SPACING), fill="x")

        self._set_amount_of_episodes()

    def _set_amount_of_episodes(self):
        amount_of_levels = len(self.level_selector.level_list.get_order())

        cycles_per_level = int(self.episodes_setting_panel.training_cycles_input.get())
        total_cycles = cycles_per_level * amount_of_levels

        self.cycles_label.configure(
            text=f"{cycles_per_level} cycles per level (total: {total_cycles})"
        )

        episodes_per_level = int(
            cycles_per_level
            * self.episodes_setting_panel.episodes_per_cycle_input.get()
        )
        total_episodes = episodes_per_level * amount_of_levels

        self.episodes_label.configure(
            text=f"{episodes_per_level} episodes per level (total: {total_episodes})"
        )
