import customtkinter as ctk
from .tools_frame.tools_frame import ToolsFrame
from .layers_group.layers_group import LayersGroup
from .layer_objects_container import LayerObjectsContainer
from editor.level import level


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

        self.layer_objects_containers = self._create_layer_objects_containers()
        self.layer_objects_container = self.layer_objects_containers[
            level.selector.get_selection("layer")
        ]

    def _create_layer_objects_containers(self):
        layer_objects_containers: dict[str, LayerObjectsContainer] = {}

        for layer in level.layers:
            layer_objects_container = LayerObjectsContainer(self, layer.name)
            layer_objects_container.pack(pady=8, anchor="w", fill="x")
            layer_objects_containers[layer.name] = layer_objects_container

        return layer_objects_containers
