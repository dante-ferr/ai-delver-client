import customtkinter as ctk
from editor.components import SvgImage
from editor.theme import theme
from editor.components.selection import populate_selection_manager, SelectionManager
from editor.level import level


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

        def _on_select(identifier: str):
            level.selector.set_selection("tool", identifier)

        populate_selection_manager(
            SelectionManager(),
            frames=self.tool_boxes,
            get_identifier=lambda tool_box: tool_box.tool_name,
            default_identifier="pencil",
            on_select=_on_select,
        )

    def _grid_tool_boxes(self):
        for i, tool_box in enumerate(self.tool_boxes):
            tool_box.grid(row=0, column=i, padx=1)

    def _create_tool_boxes(self):
        tool_size = 24

        pen_icon = SvgImage(
            svg_path="assets/svg/pencil.svg",
            size=(tool_size, tool_size),
            stroke=theme.light_icon_color,
        )
        pen_box = ToolBox(self, "pencil", pen_icon.get_ctk_image())

        eraser_icon = SvgImage(
            svg_path="assets/svg/eraser.svg",
            fill=theme.light_icon_color,
            stroke=theme.light_icon_color,
            size=(tool_size, tool_size),
        )
        eraser_box = ToolBox(self, "eraser", eraser_icon.get_ctk_image())

        return [pen_box, eraser_box]
