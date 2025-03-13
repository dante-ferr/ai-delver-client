import customtkinter as ctk
from .tools_frame.tools_frame import ToolsFrame
from .layers_panel.layers_panel import LayersPanel
from .canvas_objects_panel import CanvasObjectPanelsWrapper


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.pack_propagate(False)

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
