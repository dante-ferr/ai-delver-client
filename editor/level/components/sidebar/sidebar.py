import customtkinter as ctk
from .tools_frame.tools_frame import ToolsFrame
from .layers.layers_group import LayersGroup


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.pack_propagate(False)

        tools_frame_container = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame_container.pack(pady=8, fill="x")
        tools_frame = ToolsFrame(tools_frame_container)
        tools_frame.pack(anchor="center")

        layers_group = LayersGroup(self)
        layers_group.pack(pady=8, anchor="w", fill="x")

        # save_button = ctk.CTkButton(
        #     self, text="Save Level", command=level_editor.save_level
        # )
        # save_button.pack(pady=10, side="bottom")

        # load_button = ctk.CTkButton(
        #     self, text="Load Level", command=level_editor.load_level
        # )
        # load_button.pack(pady=10, side="bottom")
