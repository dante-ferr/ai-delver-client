import customtkinter as ctk


class LoadingLog(ctk.CTkFrame):
    """A CustomTkinter container for displaying a single loading log entry."""

    def __init__(self, parent, text: str):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)

        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate", width=50)
        self.progress_bar.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.progress_bar.start()

        self.label = ctk.CTkLabel(self, text=text, anchor="w")
        self.label.grid(row=0, column=1, padx=0, pady=5, sticky="ew")
