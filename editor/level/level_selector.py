from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from editor.level.components.sidebar.layers import LayerContainer


class LevelSelector:
    def __init__(self):
        self._selected_tool: str = "pen"
        self._selected_layer: str = "floor"
        self._selected_layer_container: LayerContainer | None = None

    @property
    def selected_tool(self):
        return self._selected_tool

    @selected_tool.setter
    def selected_tool(self, tool_name: str):
        self._selected_tool = tool_name

    @property
    def selected_layer(self):
        return self._selected_layer

    @selected_layer.setter
    def selected_layer(self, layer_name: str):
        self._selected_layer = layer_name
