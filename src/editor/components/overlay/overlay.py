import customtkinter as ctk


class Overlay(ctk.CTkToplevel):
    def __init__(self, title: str):
        from editor import app

        super().__init__(app)

        self.attributes("-topmost", True)
        self.geometry("300x150")

        self.title(title)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_reqwidth() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_reqheight() // 2)
        self.geometry(f"+{x}+{y}")

        # self.grab_set()

    def _close(self):
        # self.grab_release()
        self.destroy()
