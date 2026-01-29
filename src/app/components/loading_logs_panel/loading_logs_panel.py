import customtkinter as ctk
from ._loading_log import LoadingLog


class LoadingLogsPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for displaying training logs.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent", width=0, height=0)
        self.loading_containers: dict[str, ctk.CTkFrame] = {}

    def show_log(self, key: str, text: str):
        """
        Shows a log message with a given key.
        If a log with the same key already exists, it does nothing.
        """
        if key in self.loading_containers:
            return

        container = LoadingLog(self, text)
        container.pack(fill="x", expand=True)
        self.loading_containers[key] = container

    def remove_log(self, key: str):
        """Removes a log message identified by its key."""
        if key in self.loading_containers:
            container = self.loading_containers.pop(key)
            container.destroy()
