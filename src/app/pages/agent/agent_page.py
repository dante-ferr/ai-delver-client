from .. import Page
from .trajectory_viewer import TrajectoryViewer
from .agent_panel import AgentPanel
from .trajectory_stats_panel import TrajectoryStatsPanel

class AgentPage(Page):

    def __init__(self, master):
        super().__init__(master, "Agent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=128)
        self.grid_columnconfigure(1, weight=1, minsize=128)
        self.grid_columnconfigure(2, weight=0, minsize=256)

        agent_panel = AgentPanel(self)
        agent_panel.grid(row=0, column=0, padx=16, pady=32, sticky="nsew")

        trajectory_viewer = TrajectoryViewer(self)
        trajectory_viewer.grid(row=0, column=1, pady=32, sticky="nsew")

        trajectory_stats_panel = TrajectoryStatsPanel(self)
        trajectory_stats_panel.grid(row=0, column=2, padx=16, pady=32, sticky="nsew")
