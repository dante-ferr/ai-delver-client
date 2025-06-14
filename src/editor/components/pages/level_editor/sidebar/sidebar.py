import customtkinter as ctk
from .tools_frame.tools_frame import ToolsFrame
from .layers_panel.layers_panel import LayersPanel
from .canvas_objects_panel import CanvasObjectPanelsWrapper
from ._title_textbox import TitleTextbox
from .level_file_container import LevelFileContainer
from level_loader import level_loader


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.pack_propagate(False)

        title_textbox = TitleTextbox(self)
        title_textbox.pack(padx=0, pady=0, fill="x")

        tools_frame_container = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame_container.pack(pady=8, fill="x")
        tools_frame = ToolsFrame(tools_frame_container)
        tools_frame.pack(anchor="center")

        layersPanel = LayersPanel(self)
        layersPanel.pack(pady=8, anchor="w", fill="x")

        canvas_objects_panels_wrapper = CanvasObjectPanelsWrapper(self)
        canvas_objects_panels_wrapper.pack(
            pady=8, padx=0, anchor="w", fill="both", expand=True
        )

        grid_toggle_var = level_loader.level.toggler.get_var("grid_lines")
        grid_toggle_var.set(True)
        grid_toggle = ctk.CTkCheckBox(
            self,
            text="Grid",
            variable=grid_toggle_var,
            checkbox_width=20,
            checkbox_height=20,
        )
        grid_toggle.pack(pady=2, side="right")

        level_file_container = LevelFileContainer(self)
        level_file_container.pack(side="left", padx=2, pady=2)
