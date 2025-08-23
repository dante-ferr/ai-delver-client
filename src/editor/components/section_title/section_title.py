import customtkinter as ctk


class SectionTitle(ctk.CTkLabel):
    def __init__(self, parent, text: str):
        super().__init__(
            parent,
            text=text,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            fg_color="transparent",
        )
