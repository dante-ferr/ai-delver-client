from .replay import Replay
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from runtime.episode_trajectory import EpisodeTrajectory, DelverAction
    from level import Level


class ActionReplay(Replay):
    """
    A replay that re-simulates physics based on recorded Delver actions.
    This method is less precise but requires less data.
    """

    def __init__(self, level: "Level", trajectory: "EpisodeTrajectory"):
        # This replay mode requires client-side physics, so deterministic is True.
        super().__init__(level, trajectory, physics=True)
        self.current_action: "DelverAction | None" = None

    def update(self, dt: float):
        # Run the full physics simulation from the parent Runtime.
        super().update(dt)

        if self.finished:
            if not hasattr(self, "_final_pos_printed"):
                print("Last delver position from replay: ", self.delver.position)
                self._final_pos_printed = True
            return

        self.time_accumulator += dt

        # Determine the current action based on time.
        while self.time_accumulator >= self.time_per_action:
            if self.finished:
                break
            self.current_action = self.actions[self.current_step_index]
            self.time_accumulator -= self.time_per_action
            self.current_step_index += 1

        # Apply the action's intent.
        if self.current_action and self.current_action["move"]:
            self.delver.move(dt, self.current_action["move_angle"])

    @property
    def finished(self) -> bool:
        return self.current_step_index >= len(self.actions)

    @property
    def actions(self) -> "List[DelverAction]":
        return self.trajectory.delver_actions
