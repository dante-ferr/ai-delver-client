from src.editor.components import LoadingLogsPanel
from src.editor.components.loading_logs_panel._training_progress_log import (
    TrainingProgressLog,
)


class TrainLogsPanel(LoadingLogsPanel):

    def __init__(self, master):
        super().__init__(master)

        self.training_progress_log: TrainingProgressLog | None = None
        self.showing_training_progress = False

    def show_training_progress(self, total_episodes: int):
        if self.showing_training_progress:
            return
        self.showing_training_progress = True

        self.training_progress_log = TrainingProgressLog(self, total_episodes)
        self.training_progress_log.pack(fill="x", expand=True)

    def update_training_progress(self, current_episodes: int):
        if self.training_progress_log:
            self.training_progress_log.update_progress(current_episodes)

    def remove_training_progress(self):
        if not self.showing_training_progress:
            return
        self.showing_training_progress = False

        if self.training_progress_log:
            self.training_progress_log.destroy()
            self.training_progress_log = None
