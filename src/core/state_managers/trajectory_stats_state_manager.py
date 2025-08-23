from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import customtkinter as ctk
    from src.editor.components import LoadingLogsPanel


class TrajectoryStatsStateManager:
    def __init__(self):
        self._getting_stats = False
        self.disable_on_get_stats_elements: "set[ctk.CTkBaseClass]" = set()
        self.stats_logs_panel: "LoadingLogsPanel | None" = None
        self.on_refresh_stats_callbacks: list[Callable[[], None]] = []

    def add_on_refresh_stats_callback(self, callback: Callable[[], None]):
        self.on_refresh_stats_callbacks.append(callback)

    def refresh_stats(self):
        for callback in self.on_refresh_stats_callbacks:
            callback()

    def set_stats_logs_panel(self, panel: "LoadingLogsPanel"):
        self.stats_logs_panel = panel
        self._update_ui_state()

    def add_disable_on_get_stats_element(self, element: "ctk.CTkBaseClass"):
        self.disable_on_get_stats_elements.add(element)
        self._update_ui_state()

    def _update_ui_state(self):
        is_busy = self._getting_stats

        state_for_disable_elements = "disabled" if is_busy else "normal"
        for element in self.disable_on_get_stats_elements:
            element.configure(state=state_for_disable_elements)

        if self.stats_logs_panel:
            if self._getting_stats:
                self.stats_logs_panel.show_log("getting_stats", "Getting statistics...")
            else:
                self.stats_logs_panel.remove_log("getting_stats")

    def reset_states(self):
        self._getting_stats = False
        self._update_ui_state()

    @property
    def getting_stats(self):
        return self._getting_stats

    @getting_stats.setter
    def getting_stats(self, value: bool):
        if self._getting_stats == value:
            return
        self._getting_stats = value
        self._update_ui_state()


trajectory_stats_state_manager = TrajectoryStatsStateManager()
