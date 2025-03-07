import customtkinter as ctk
from typing import TYPE_CHECKING
from .tools_frame import ToolsFrame
from .layer_container import LayerContainer

if TYPE_CHECKING:
    from level_editor.level_editor import LevelEditor


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent: "LevelEditor"):
        super().__init__(parent, width=640, border_width=0)

        level_editor = parent

        tools_frame = ToolsFrame(self, level_editor)
        tools_frame.pack()

        layer_container = LayerContainer(self)
        layer_container.pack(pady=20)

        save_button = ctk.CTkButton(
            self, text="Save Level", command=level_editor.save_level
        )
        save_button.pack(pady=10, side="bottom")

        load_button = ctk.CTkButton(
            self, text="Load Level", command=level_editor.load_level
        )
        load_button.pack(pady=10, side="bottom")
