import customtkinter as ctk


class TrainingProgressLog(ctk.CTkFrame):
    """A CustomTkinter container for displaying training progress."""

    def __init__(self, parent, total_episodes: int):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        self.total_episodes = total_episodes

        self.label = ctk.CTkLabel(self, text="", anchor="w")
        self.label.grid(row=0, column=0, padx=0, pady=2, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate")
        self.progress_bar.grid(row=1, column=0, padx=0, pady=(0, 5), sticky="ew")
        self.progress_bar.set(0)

        self.update_progress(0)

    def update_progress(self, current_episodes: int):
        progress = (
            current_episodes / self.total_episodes if self.total_episodes > 0 else 0
        )
        self.progress_bar.set(progress)
        self.label.configure(
            text=f"Training in progress... ({current_episodes}/{self.total_episodes})"
        )
