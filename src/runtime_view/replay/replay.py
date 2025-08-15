from ..viewable_runtime import ViewableRuntime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from runtime.episode_trajectory import EpisodeTrajectory
    from level import Level
    from runtime.episode_trajectory import DelverAction


# Last delver position from training simulation:    (160.6585689460665, 117.5434652429483)

class Replay(ViewableRuntime):

    def __init__(self, level: "Level", trajectory: "EpisodeTrajectory"):
        super().__init__(level, deterministic=True)
        self.trajectory = trajectory

        if self.actions_per_second > 0:
            self.time_per_action = 1.0 / self.actions_per_second
        else:
            self.time_per_action = float("inf")

        # State for managing replay time
        self.time_accumulator = 0.0
        self.current_action_index = 0

        self.current_action: "None | DelverAction" = None

    def update(self, dt):
        # Call parent update, but ensure it doesn't also move the delver
        super().update(dt)

        if self.finished:
            if not hasattr(self, "_final_pos_printed"):
                print("Last delver position from replay: ", self.delver.position)
                self._final_pos_printed = True
            return

        self.time_accumulator += dt

        # This loop processes all actions that should have occurred during the elapsed frame time.
        # This makes the replay logic independent of the frame rate and ensures correctness.
        while self.time_accumulator >= self.time_per_action:
            if self.finished:
                break

            # Get the action for the current logical step
            self.current_action = self.actions[self.current_action_index]

            # Decrease accumulator and advance to the next action
            self.time_accumulator -= self.time_per_action
            self.current_action_index += 1

        if self.current_action:
            if self.current_action["move"]:
                self.delver.move(dt, self.current_action["move_angle"])

        if self.delver.check_collision(self.goal):
            print("GOAL COLLISION")

    @property
    def finished(self):
        return self.current_action_index >= len(self.actions)

    @property
    def actions_per_second(self):
        return self.trajectory.actions_per_second

    @property
    def actions(self):
        return self.trajectory.delver_actions


# from ..viewable_runtime import ViewableRuntime
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from runtime.episode_trajectory import EpisodeTrajectory, DelverAction
#     from level import Level


# def lerp(a: float, b: float, alpha: float) -> float:
#     """
#     Linearly interpolates between two values 'a' and 'b' by a factor 'alpha'.
#     """
#     return a + alpha * (b - a)


# # Last Delver position from training simulation:  (160.6585689460665, 117.5434652429483)
# # Last delver position from replay simulation:  (111.92140387261585, 103.26581553136683)
# # Last delver position from replay simulation (attempt 2 with the same trajectory):  (122.21053789333104, 108.43550995775782)
# # Last delver position from replay simulation (attempt 3 with the same trajectory):  (125.22434065659793, 104.7964881542073)

# class Replay(ViewableRuntime):

#     def __init__(self, level: "Level", trajectory: "EpisodeTrajectory"):
#         super().__init__(level)
#         self.trajectory = trajectory

#         if self.actions_per_second > 0:
#             self.time_per_action = 1.0 / self.actions_per_second
#         else:
#             self.time_per_action = float("inf")

#         # State for managing replay time
#         self.time_accumulator = 0.0
#         self.current_action_index = 0

#     def update(self, dt):
#         super().update(dt)

#         if self.finished:
#             final_action = self.actions[-1]
#             if final_action["move"] == False:
#                 # For movement, we likely just stop.
#                 # For position, you might snap to a final recorded position.
#                 pass
#             print("Last delver position: ", self.delver.position)
#             return

#         self.time_accumulator += dt

#         # Advance our state index if enough time has passed
#         # This loop handles lag spikes by processing multiple state changes in one frame if needed.
#         while self.time_accumulator >= self.time_per_action:
#             self.time_accumulator -= self.time_per_action
#             self.current_action_index += 1

#             if self.finished:
#                 return

#         # Determine the states to interpolate between (previous and next)
#         # The "previous" state is the one before our target index.
#         # Handle the edge case for the very first frame.
#         prev_index = max(0, self.current_action_index - 1)
#         next_index = self.current_action_index
#         prev_action = self.actions[prev_index]
#         next_action = self.actions[next_index]

#         self._handle_delver_move(prev_action, next_action, dt)
#         if self.delver.check_collision(self.goal):
#             print("GOAL COLLISION")

#     def _handle_delver_move(
#         self, prev_action: "DelverAction", next_action: "DelverAction", dt: float
#     ):
#         # # Calculate the interpolation factor 'alpha'
#         # # This is how far we are (0.0 to 1.0) into the current time slice.
#         # alpha = self.time_accumulator / self.time_per_action

#         # # Interpolate the values and apply them
#         # # We only interpolate if both states are "moving".
#         # if prev_action["move"] and next_action["move"]:
#         #     # Interpolate the movement angle
#         #     prev_angle = prev_action.get("move_angle", 0.0)
#         #     next_angle = next_action.get("move_angle", 0.0)

#         #     interpolated_angle = lerp(prev_angle, next_angle, alpha)

#         #     # Now, move the character using the smooth, interpolated angle
#         #     self.delver.move(dt, interpolated_angle)

#         # elif next_action["move"]:
#         #     # If we just started moving, just use the next action's angle
#         #     self.delver.move(dt, next_action["move_angle"])

#         if next_action["move"]:
#             # If we just started moving, just use the next action's angle
#             self.delver.move(dt, next_action["move_angle"])

#     @property
#     def finished(self):
#         return self.current_action_index >= len(self.actions)

#     @property
#     def actions_per_second(self):
#         return self.trajectory.actions_per_second

#     @property
#     def actions(self):
#         return self.trajectory.delver_actions
