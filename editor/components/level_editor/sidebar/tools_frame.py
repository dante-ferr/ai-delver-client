import customtkinter as ctk
from ...svg_image import SvgImage
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from level_editor.level_editor import LevelEditor


class ToolsFrame(ctk.CTkFrame):
    def __init__(self, parent, level_editor: "LevelEditor"):
        super().__init__(parent)

        tool_size = 16
        pen_icon = SvgImage(svg_path="assets/svg/pen.svg", size=(tool_size, tool_size))
        eraser_icon = SvgImage(
            svg_path="assets/svg/eraser.svg",
            fill="#000000",
            size=(tool_size, tool_size),
        )

        self.pen_button = ctk.CTkButton(
            self,
            image=pen_icon,
            text="",
            command=level_editor.select_pen,
            width=32,
            height=32,
        )
        self.pen_button.pack(side="left", padx=5, pady=10)

        self.eraser_button = ctk.CTkButton(
            self,
            image=eraser_icon,
            text="",
            command=level_editor.select_eraser,
            width=32,
            height=32,
        )
        self.eraser_button.pack(side="left", padx=5, pady=10)
