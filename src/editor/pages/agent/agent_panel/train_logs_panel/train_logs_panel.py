import customtkinter as ctk


class TrainLogContainer(ctk.CTkFrame):
    """A CustomTkinter container for displaying a single training log entry."""

    def __init__(self, parent, text: str):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate", width=50)
        self.progress_bar.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.progress_bar.start()

        self.label = ctk.CTkLabel(self, text=text, anchor="w")
        self.label.grid(row=0, column=1, padx=0, pady=5, sticky="ew")


class TrainLogsPanel(ctk.CTkFrame):
    """
    A CustomTkinter panel for displaying training logs.
    """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.log_containers: dict[str, TrainLogContainer] = {}

    def show_log(self, key: str, text: str):
        """
        Shows a log message with a given key.
        If a log with the same key already exists, it does nothing.
        """
        if key in self.log_containers:
            return

        container = TrainLogContainer(self, text)
        container.pack(fill="x", expand=True)
        self.log_containers[key] = container

    def remove_log(self, key: str):
        """Removes a log message identified by its key."""
        if key in self.log_containers:
            container = self.log_containers.pop(key)
            container.destroy()
