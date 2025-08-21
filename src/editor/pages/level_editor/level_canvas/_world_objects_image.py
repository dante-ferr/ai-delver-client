import customtkinter as ctk
from PIL import ImageTk
from typing import cast
from ..level_editor_manager import level_editor_manager

class WorldObjectsImage:
    def __init__(self):
        self.images: dict[str, ImageTk.PhotoImage] = {}

    def get_image(self, canvas_object_name: str) -> ctk.CTkImage:
        if canvas_object_name not in self.images:
            canvas_object = level_editor_manager.objects_manager.get_canvas_object(
                canvas_object_name
            )
            if not canvas_object:
                raise KeyError(f"Canvas object '{canvas_object_name}' not found.")
            self.images[canvas_object_name] = ImageTk.PhotoImage(canvas_object.image)

        return cast("ctk.CTkImage", self.images[canvas_object_name])
