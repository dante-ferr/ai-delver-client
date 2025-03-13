from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from editor.level.components.sidebar.layers_panel import LayerContainer


class LevelSelector:
    def __init__(self):
        self._selections: dict[str, str] = {}
        self._selection_callbacks: dict[str, Callable[[str], None]] = {}

    def set_selection(self, selection_name: str, selection_value: str):
        # print(f"Setting selection {selection_name} to {selection_value}")
        self._selections[selection_name] = selection_value

        callback = self._selection_callbacks.get(selection_name)
        if callback is not None:
            callback(selection_value)

    def get_selection(self, selection_name: str) -> str:
        return self._selections[selection_name]

    def set_select_callback(self, selection_name: str, callback: Callable[[str], None]):
        self._selection_callbacks[selection_name] = callback
