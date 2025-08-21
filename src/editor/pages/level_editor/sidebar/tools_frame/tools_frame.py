import customtkinter as ctk
from editor.components import SvgImage
from editor.theme import theme
from editor.utils.selection import populate_selection_manager, SelectionManager
from ...level_editor_manager import level_editor_manager
from src.config import ASSETS_PATH


class ToolBox(ctk.CTkFrame):
    def __init__(self, parent, tool_name: str, icon_image: ctk.CTkImage):
        super().__init__(parent)
        self.tool_name = tool_name

        label = ctk.CTkLabel(self, image=icon_image, text="")
        label.pack(padx=4.8, pady=4.8)


class ToolsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.tool_boxes = self._create_tool_boxes()

        self._grid_tool_boxes()

        def _on_select(frame: "ToolBox"):
            level_editor_manager.selector.set_selection("tool", frame.tool_name)

        populate_selection_manager(
            SelectionManager(),
            frames=self.tool_boxes,
            default_frame=self.tool_boxes[0],
            on_select=_on_select,
        )

    def _grid_tool_boxes(self):
        for i, tool_box in enumerate(self.tool_boxes):
            tool_box.grid(row=0, column=i, padx=1)

    def _create_tool_boxes(self):
        tool_size = 24

        pen_icon = SvgImage(
            svg_path=str(ASSETS_PATH / "svg" / "pencil.svg"),
            size=(tool_size, tool_size),
            stroke=theme.icon_color,
        )
        pen_box = ToolBox(self, "pencil", pen_icon.get_ctk_image())

        eraser_icon = SvgImage(
            svg_path=str(ASSETS_PATH / "svg" / "eraser.svg"),
            fill=theme.icon_color,
            stroke=theme.icon_color,
            size=(tool_size, tool_size),
        )
        eraser_box = ToolBox(self, "eraser", eraser_icon.get_ctk_image())

        return [pen_box, eraser_box]
