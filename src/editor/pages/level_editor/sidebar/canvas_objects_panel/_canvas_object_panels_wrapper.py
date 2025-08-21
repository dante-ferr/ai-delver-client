import customtkinter as ctk
from .canvas_objects_panel import CanvasObjectsPanel
from typing import cast
from ...level_editor_manager import level_editor_manager


class CanvasObjectPanelsWrapper(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.current_canvas_objects_panel: CanvasObjectsPanel | None = None
        self.canvas_objects_panels = self._create_canvas_objects_panels()
        self._set_current_canvas_objects_panel_by_layer_name(
            level_editor_manager.selector.get_selection("layer")
        )
        level_editor_manager.selector.set_select_callback(
            "layer", self._on_layer_select
        )

    def _create_canvas_objects_panels(self):
        canvas_objects_panels: dict[str, CanvasObjectsPanel] = {}

        for layer in level_editor_manager.objects_manager.layers:
            panel = CanvasObjectsPanel(self, layer.name, max_height=400)
            canvas_objects_panels[layer.name] = panel

        return canvas_objects_panels

    def _on_layer_select(self, layer_name: str):
        self._set_current_canvas_objects_panel_by_layer_name(layer_name)

        current_canvas_objects_panel = cast(
            CanvasObjectsPanel, self.current_canvas_objects_panel
        )
        self.configure(height=current_canvas_objects_panel.winfo_height())

    def _set_current_canvas_objects_panel_by_layer_name(self, layer_name: str):
        if self.current_canvas_objects_panel is not None:
            self.current_canvas_objects_panel.pack_forget()

        self.current_canvas_objects_panel = self.canvas_objects_panels[layer_name]
        self.current_canvas_objects_panel.pack(
            pady=8, anchor="w", fill="both", expand=True
        )
