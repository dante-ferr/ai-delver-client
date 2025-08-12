import customtkinter as ctk
from PIL import ImageTk
from typing import cast


class WorldObjectsImage:
    def __init__(self):
        self.images: dict[str, ImageTk.PhotoImage] = {}

        self._initialize_images()

    def _initialize_images(self):
        """Initialize the images from the images directory."""
        from level_loader import level_loader

        for canvas_object in level_loader.level.map.canvas_objects.values():
            self.images[canvas_object.name] = ImageTk.PhotoImage(canvas_object.image)

    def get_image(self, canvas_object_name: str) -> ctk.CTkImage:
        return cast("ctk.CTkImage", self.images[canvas_object_name])
