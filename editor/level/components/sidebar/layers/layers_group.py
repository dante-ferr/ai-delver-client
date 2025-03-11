import customtkinter as ctk
from .layer_container import LayerContainer
from editor.components.svg_image import SvgImage
from editor.theme import theme
from editor.components.selection import populate_selection_manager, SelectionManager


class LayersGroup(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        title = ctk.CTkLabel(
            self,
            text="Layers",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title.pack(pady=8, side="top", anchor="w")

        self.layer_containers: list[LayerContainer] = self._create_layer_containers()

        self._pack_layer_containers()
        populate_selection_manager(
            SelectionManager(),
            frames=self.layer_containers,
            get_identifier=lambda layer_container: layer_container.layer_name,
            attribute_name="selected_layer",
            default_identifier="floor",
        )

    def _pack_layer_containers(self):
        for layer_container in self.layer_containers:
            layer_container.pack(side="top", padx=8, anchor="w", fill="x")

    def _create_layer_containers(self):
        layer_icon_size = 24
        wall_icon = SvgImage(
            svg_path="assets/svg/layers/walls.svg",
            size=(layer_icon_size, layer_icon_size),
            fill=theme.light_icon_color,
        )
        walls_container = LayerContainer(self, "walls", wall_icon.get_ctk_image())

        floor_icon = SvgImage(
            svg_path="assets/svg/layers/floor.svg",
            size=(layer_icon_size, layer_icon_size),
            fill=theme.light_icon_color,
        )
        floor_container = LayerContainer(self, "floor", floor_icon.get_ctk_image())

        return [walls_container, floor_container]
