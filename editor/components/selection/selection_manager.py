from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .selection_element_group import SelectionElementGroup


class SelectionManager:
    def __init__(
        self,
        initial_selection_element_group: "SelectionElementGroup | None" = None,
        active_color=("gray75", "gray25"),
        inactive_color="transparent",
    ):
        self._selected_element_group = initial_selection_element_group

        self.selection_element_groups: list[SelectionElementGroup] = []

        self.active_color = active_color
        self.inactive_color = inactive_color

    def add_selection_element_group(
        self, selection_element_group: "SelectionElementGroup"
    ):
        selection_element_group.set_colors(self.active_color, self.inactive_color)
        selection_element_group.set_manager(self)
        self.selection_element_groups.append(selection_element_group)

    @property
    def selected_element_group(self):
        return self._selected_element_group

    @selected_element_group.setter
    def selected_element_group(self, selection_element_group: "SelectionElementGroup"):
        if self._selected_element_group:
            self._selected_element_group.deselect()
        self._selected_element_group = selection_element_group

        selection_element_group.select()
        selection_element_group.on_select()
