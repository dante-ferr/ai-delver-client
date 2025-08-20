import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from canvas_controller.canvas_objects import CanvasObject


class CanvasObjectContainer(ctk.CTkFrame):
    image_size = (32, 32)

    def __init__(self, parent, canvas_object: "CanvasObject"):
        super().__init__(parent, fg_color="transparent")
        self.canvas_object = canvas_object

        image = ctk.CTkImage(canvas_object.image, size=self.image_size)
        label = ctk.CTkLabel(self, image=image, text="")
        label.pack(padx=3.2, pady=3.2)
