import customtkinter as ctk
from editor.components.overlay.message_overlay import MessageOverlay
import json
from agent_loader import agent_loader
from editor.utils import verify_level_issues
from app_manager import app_manager

class TrajectoryViewer(ctk.CTkFrame):
    DISPLAY_TRAJECTORY_JSON = True

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=8, pady=(8, 4), sticky="w")

        self.index_entry = ctk.CTkEntry(
            input_frame, placeholder_text="Trajectory Index", width=128
        )
        self.index_entry.grid(row=0, column=0, padx=4, pady=4)

        load_button = ctk.CTkButton(
            input_frame, text="Load", command=self._load_trajectory, width=128
        )
        load_button.grid(row=0, column=1, padx=4, pady=4)

        replay_button = ctk.CTkButton(
            input_frame, text="Replay", command=lambda: self._replay()
        )
        replay_button.grid(row=0, column=2, padx=4, pady=4)

        self.data_display = ctk.CTkTextbox(self, wrap="none")
        self.data_display.grid(row=1, column=0, padx=8, pady=(4, 8), sticky="nsew")
        self._set_data_display_to_default()
        self.data_display.configure(state="disabled")

    def _replay(self):
        if not verify_level_issues():
            app_manager.start_replay()

    def _load_trajectory(self):
        index_str = self.index_entry.get()
        if not index_str:
            MessageOverlay("Please enter a trajectory index.", subject="Error")
            return

        try:
            index = int(index_str)
        except ValueError:
            MessageOverlay("Index must be an integer.", subject="Error")
            return

        self.trajectory = self.trajectory_loader.load_trajectory(index)
        if self.trajectory is None:
            MessageOverlay(
                f"Trajectory with index '{index}' not found.", subject="Error"
            )
            self._set_data_display_to_default()
            return

        if TrajectoryViewer.DISPLAY_TRAJECTORY_JSON:
            self._display_trajectory_json(index)
        else:
            self._display_trajectory_data(index)

    def _display_trajectory_data(self, index):
        pass

    def _display_trajectory_json(self, index):
        if self.trajectory is None:
            raise ValueError("Trajectory is not loaded.")
        trajectory_json_str = self.trajectory.to_json()

        self.data_display.configure(state="normal")
        self.data_display.delete("1.0", "end")

        try:
            parsed_json = json.loads(trajectory_json_str)
            formatted_json = json.dumps(parsed_json, indent=4)
            self.data_display.insert("1.0", formatted_json)
        except json.JSONDecodeError:
            MessageOverlay(
                f"Error decoding trajectory data for index '{index}'.", subject="Error"
            )
            self.data_display.insert("1.0", "Failed to load trajectory data.")

        self.data_display.configure(state="disabled")

    def _set_data_display_to_default(self):
        self.data_display.insert(
            "1.0",
            "Trajectory data will be shown here. Make sure to train the agent before searching for a trajectory.",
        )

    @property
    def trajectory_loader(self):
        return agent_loader.agent.trajectory_loader
