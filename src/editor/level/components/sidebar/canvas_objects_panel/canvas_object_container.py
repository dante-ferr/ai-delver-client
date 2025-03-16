import customtkinter as ctk
from typing import TYPE_CHECKING
from PIL import Image

if TYPE_CHECKING:
    from editor.level.canvas_object import CanvasObject


class CanvasObjectContainer(ctk.CTkFrame):
    image_size = (32, 32)

    def __init__(self, parent, canvas_object: "CanvasObject"):
        super().__init__(parent, fg_color="transparent")
        self.canvas_object = canvas_object

        image = ctk.CTkImage(
            light_image=Image.open(canvas_object.image_path), size=self.image_size
        )
        label = ctk.CTkLabel(self, image=image, text="")
        label.pack(padx=3.2, pady=3.2)
