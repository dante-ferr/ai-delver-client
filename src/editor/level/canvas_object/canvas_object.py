from typing import Callable
import customtkinter as ctk
from PIL import Image


class CanvasObject:
    def __init__(
        self, name: str, image_path: str, click_callback: Callable, unique: bool = False
    ):
        self.name = name
        self.click_callback = click_callback
        self.unique = unique

        self.image = Image.open(image_path)
