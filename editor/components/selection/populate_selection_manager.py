from typing import Callable, List, Any
from editor.components.selection import SelectionManager, SelectionElementGroup
from editor.level import level


def populate_selection_manager(
    selection_manager: SelectionManager,
    frames: List[Any],
    get_identifier: Callable[[Any], str],
    attribute_name: str,
    default_identifier: str,
):
    """Factory for creating configured SelectionManager instances.

    Args:
        frames: List of UI frames to manage
        get_identifier: Function to extract identifier from a frame
        attribute_name: Level attribute name to modify on selection
        default_identifier: Default frame identifier to select
    """
    default_group = None

    for frame in frames:
        identifier = get_identifier(frame)

        def _on_select(current_id: str = identifier):
            setattr(level, attribute_name, current_id)

        group = SelectionElementGroup(_on_select, frame)
        selection_manager.add_selection_element_group(group)

        if identifier == default_identifier:
            default_group = group

    if not default_group:
        raise ValueError(f"No frame found with identifier '{default_identifier}'")

    selection_manager.selected_element_group = default_group
