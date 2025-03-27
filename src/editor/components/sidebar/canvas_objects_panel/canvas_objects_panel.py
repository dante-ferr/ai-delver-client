from editor.utils.selection import populate_selection_manager, SelectionManager
from level import level_loader
from ._canvas_object_container import CanvasObjectContainer
from typing import TYPE_CHECKING
from editor.theme import theme
from editor.components import MouseWheelScrollableFrame

if TYPE_CHECKING:
    from level.grid_map.editor_tilemap.editor_tilemap_layer import (
        EditorTilemapLayer,
    )
    from level.grid_map.world_objects_map import WorldObjectsLayer
    from editor.utils.selection.selection_element_group import SelectionElementGroup


class CanvasObjectsPanel(MouseWheelScrollableFrame):
    def __init__(
        self, parent, layer: "EditorTilemapLayer | WorldObjectsLayer", *args, **kwargs
    ):
        super().__init__(parent, *args, fg_color="transparent", **kwargs)

        self.layer = layer

        self.configure(border_width=0)

        self.canvas_object_containers = self._create_canvas_object_containers()
        if len(self.canvas_object_containers) == 0:
            return

        for i, container in enumerate(self.canvas_object_containers):
            row, column = divmod(i, 4)
            container.grid(row=row, column=column, sticky="nsew")

        selection_manager = SelectionManager(
            activate_callback=self._object_activate_callback,
            deactivate_callback=self._object_deactivate_callback,
        )

        def _on_select(frame: "CanvasObjectContainer"):
            level_loader.level.selector.set_selection(
                layer.name + ".canvas_object", frame.canvas_object.name
            )

        populate_selection_manager(
            selection_manager,
            frames=self.canvas_object_containers,
            default_frame=self.canvas_object_containers[0],
            on_select=_on_select,
        )

        self._update_scrollbar_visibility()

    def _get_canvas_object_identifier(
        self, canvas_object_container: "CanvasObjectContainer"
    ):
        return canvas_object_container.canvas_object.name

    def _object_activate_callback(
        self, selection_element_group: "SelectionElementGroup"
    ):
        selection_element_group.frame.configure(
            border_width=1, border_color=theme.select_border_color
        )

    def _object_deactivate_callback(
        self, selection_element_group: "SelectionElementGroup"
    ):
        selection_element_group.frame.configure(border_width=0)

    def _create_canvas_object_containers(self):
        canvas_object_containers: list[CanvasObjectContainer] = []

        for canvas_object in self.layer.canvas_object_manager.canvas_objects.values():
            canvas_object_containers.append(CanvasObjectContainer(self, canvas_object))

        return canvas_object_containers
