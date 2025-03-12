import customtkinter as ctk
from .layer_container import LayerContainer
from editor.components.svg_image import SvgImage
from editor.theme import theme
from editor.components.selection import populate_selection_manager, SelectionManager
from editor.level import level


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

        def _on_select(identifier: str):
            level.selector.set_selection("layer", identifier)

        populate_selection_manager(
            SelectionManager(),
            frames=self.layer_containers,
            get_identifier=lambda layer_container: layer_container.layer_name,
            default_identifier="floor",
            on_select=_on_select,
        )

    def _pack_layer_containers(self):
        for layer_container in self.layer_containers:
            layer_container.pack(side="top", padx=8, anchor="w", fill="x")

    def _create_layer_containers(self):
        essentials_container = self._create_layer_container(
            "assets/svg/important.svg", "essentials"
        )
        walls_container = self._create_layer_container("assets/svg/walls.svg", "walls")
        floor_container = self._create_layer_container("assets/svg/floor.svg", "floor")

        return [essentials_container, walls_container, floor_container]

    def _create_layer_container(self, svg_path: str, layer_name: str):
        layer_icon_size = 24
        icon = SvgImage(
            svg_path=svg_path,
            size=(layer_icon_size, layer_icon_size),
            fill=theme.light_icon_color,
        )
        container = LayerContainer(self, layer_name, icon.get_ctk_image())
        return container
