import customtkinter as ctk
from pytiling import Tilemap
import pickle


class LayerContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        create_layer_button = ctk.CTkButton(self, text="Add Layer")
        create_layer_button.pack(pady=10)
