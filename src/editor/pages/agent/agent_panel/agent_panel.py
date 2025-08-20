import customtkinter as ctk
from ._agent_title_textbox import AgentTitleTextbox
from .agent_file_container import AgentFileContainer
from .train_container import TrainContainer
from training_manager import training_manager

class AgentPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for creating, editing, saving, and loading Agents.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        title_textbox = AgentTitleTextbox(self)
        title_textbox.pack(padx=0, pady=0, fill="x")

        train_container = TrainContainer(self)
        train_container.pack(padx=2, pady=2)

        self.episodes_label = ctk.CTkLabel(self, text="Episodes: 100")
        self.episodes_label.pack(pady=0, anchor="w", fill="x")
        self.episodes_slider = ctk.CTkSlider(
            self, from_=10, to=1000, width=200, height=20
        )
        self.episodes_slider.pack(pady=(0, 24))
        self._set_amount_of_episodes(50)

        self.episodes_slider.configure(command=self._on_episode_slide)

        agent_file_container = AgentFileContainer(self)
        agent_file_container.pack(side="bottom", padx=2, pady=2)

    def _on_episode_slide(self, value):
        rounded_value = round(value / 10) * 10
        self._set_amount_of_episodes(rounded_value)

    def _set_amount_of_episodes(self, value):
        self.episodes_slider.set(value)
        self.episodes_label.configure(text=f"Episodes: {value}")
        training_manager.amount_of_episodes = value
