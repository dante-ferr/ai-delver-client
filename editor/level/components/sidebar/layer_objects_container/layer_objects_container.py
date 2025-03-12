from editor.components.selection import populate_selection_manager
import customtkinter as ctk


class LayerObjectsContainer(ctk.CTkFrame):
    def __init__(self, parent, layer_name: str):
        super().__init__(parent, fg_color="transparent")
        self.layer_name = layer_name
