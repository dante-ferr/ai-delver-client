from typing import Callable, List, Any
from editor.components.selection import SelectionManager, SelectionElementGroup
from editor.level import level


def populate_selection_manager(
    selection_manager: SelectionManager,
    frames: List[Any],
    get_identifier: Callable[[Any], str],
    default_identifier: str,
    on_select: Callable[[str], None],
):
    """Factory for creating configured SelectionManager instances.

    Args:
        selection_manager: The SelectionManager instance to configure.
        frames: A list of frames to add to the SelectionManager.
        get_identifier: A function that takes a frame and returns its identifier.
        default_identifier: The identifier of the frame that should be selected by default.
        on_select: A function that takes the identifier of the selected frame and does something with it.
    """
    default_group = None

    for frame in frames:
        identifier = get_identifier(frame)

        def _on_select(identifier=identifier):
            on_select(identifier)

        group = SelectionElementGroup(_on_select, frame)
        selection_manager.add_selection_element_group(group)

        if identifier == default_identifier:
            default_group = group

    if not default_group:
        raise ValueError(f"No frame found with identifier '{default_identifier}'")

    selection_manager.selected_element_group = default_group
