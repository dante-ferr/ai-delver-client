import customtkinter as ctk
from .tools_frame.tools_frame import ToolsFrame
from .layers_panel.layers_panel import LayersPanel
from .canvas_objects_panel import CanvasObjectPanelsWrapper
from ._level_title_textbox import LevelTitleTextbox
from .level_file_container import LevelFileContainer
from level_loader import level_loader
from editor.utils import verify_level_issues
from src.editor.components import SectionTitle
from typing import cast

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        from src.core.state_managers import canvas_state_manager
        from ..level_editor_manager import level_editor_manager

        level_editor_manager.objects_manager.assign_level_to_objects(level_loader.level)

        super().__init__(parent, fg_color="transparent")

        self.pack_propagate(False)

        level_editor_manager.selector.set_selection("layer", "platforms")

        title_textbox = LevelTitleTextbox(self)
        title_textbox.pack(padx=0, pady=0, fill="x")

        test_level_button = ctk.CTkButton(
            self, text="Test Level", command=self._test_level
        )
        test_level_button.pack(pady=8)

        layersPanel = LayersPanel(self)
        layersPanel.pack(pady=(8, 32), anchor="w", fill="x")

        edit_label = SectionTitle(self, text="Edit")
        edit_label.pack(pady=4, side="top", anchor="w")

        tools_frame_container = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame_container.pack(pady=2, fill="x")
        tools_frame = ToolsFrame(tools_frame_container)
        tools_frame.pack(anchor="center")

        canvas_objects_panels_wrapper = CanvasObjectPanelsWrapper(self)
        canvas_objects_panels_wrapper.pack(
            pady=8, padx=0, anchor="w", fill="both", expand=True
        )

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x")

        grid_toggle_var = cast(ctk.BooleanVar, canvas_state_manager.vars["grid_lines"])
        grid_toggle_var.set(True)
        grid_toggle = ctk.CTkCheckBox(
            bottom_frame,
            text="Grid",
            variable=grid_toggle_var,
            checkbox_width=20,
            checkbox_height=20,
        )
        grid_toggle.pack(pady=2, side="right")

        level_file_container = LevelFileContainer(bottom_frame)
        level_file_container.pack(side="left", padx=2, pady=2)

    def _test_level(self):
        from app_manager import app_manager

        if not verify_level_issues():
            app_manager.start_game()
