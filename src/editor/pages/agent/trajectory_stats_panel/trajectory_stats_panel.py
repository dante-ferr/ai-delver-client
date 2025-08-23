from runtime.episode_trajectory import TrajectoryStatsCalculator
import customtkinter as ctk
import asyncio
import threading
from trajectory_stats_state_manager import trajectory_stats_state_manager
from src.editor.components import LoadingLogsPanel, SectionTitle

# TODO: Make the amount of trajectories display immediate (as the TrajectoryStatsCalculator has a sync
# method called 'get_amount_of_trajectories').


class TrajectoryStatsPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", width=256, **kwargs)

        title = SectionTitle(self, text="Trajectory Stats")
        title.pack(pady=(0, 8), side="top", anchor="w")

        fetch_container = ctk.CTkFrame(self)
        fetch_container.pack(fill="x", pady=(0, 8))

        get_stats_button = ctk.CTkButton(
            fetch_container, text="Get stats", command=self._start_get_stats_thread
        )
        get_stats_button.grid(row=0, column=1, padx=(0, 8), pady=0, sticky="n")
        trajectory_stats_state_manager.add_disable_on_get_stats_element(
            get_stats_button
        )

        stats_logs_panel = LoadingLogsPanel(fetch_container)
        stats_logs_panel.grid(row=0, column=2, padx=(8, 0), sticky="ew")
        trajectory_stats_state_manager.set_stats_logs_panel(stats_logs_panel)

        self.stats_container = ctk.CTkFrame(self)
        self.stats_container.pack(fill="both", expand=True)

        trajectory_stats_state_manager.add_on_refresh_stats_callback(
            self._start_get_stats_thread
        )
        self._start_get_stats_thread()

    def _start_get_stats_thread(self):
        thread = threading.Thread(
            target=lambda: asyncio.run(self._get_stats()), daemon=True
        )
        thread.start()

    async def _get_stats(self):
        from agent_loader import agent_loader

        trajectory_stats_state_manager.getting_stats = True

        # Yield control to the event loop briefly. This allows the UI update from
        # setting getting_stats to True to be processed by the main GUI thread
        # before the potentially long-running get_stats() call begins.
        await asyncio.sleep(0.01)

        try:
            stats_calculator = TrajectoryStatsCalculator(agent_loader.agent.name)
            stats = await stats_calculator.get_stats()

            for widget in self.stats_container.winfo_children():
                widget.destroy()

            for stat_name, stat_value in stats.items():
                label = ctk.CTkLabel(
                    self.stats_container, text=f"{stat_name.capitalize()}: {stat_value}"
                )
                label.pack(anchor="w", padx=4, pady=2)
        finally:
            trajectory_stats_state_manager.getting_stats = False
