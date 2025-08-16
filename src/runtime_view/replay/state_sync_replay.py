from .replay import Replay
from typing import TYPE_CHECKING, Dict, cast, List
from pymunk import Vec2d
from runtime.world_objects.entities.entity import Entity
from runtime.episode_trajectory.snapshots import interpolate_frame_snapshots

if TYPE_CHECKING:
    from runtime.episode_trajectory import EpisodeTrajectory
    from runtime.episode_trajectory.snapshots import FrameSnapshot
    from level import Level


def lerp(a: float, b: float, alpha: float) -> float:
    return a + alpha * (b - a)


def lerp_vec(v1: list[float], v2: list[float], alpha: float) -> Vec2d:
    return Vec2d(v1[0], v1[1]).interpolate_to(Vec2d(v2[0], v2[1]), alpha)


class StateSyncReplay(Replay):
    """
    A 100% accurate replay that reads full physics state snapshots from the
    trajectory and interpolates them for smooth visuals. It does not run
    its own physics simulation.
    """

    def __init__(self, level: "Level", trajectory: "EpisodeTrajectory"):
        # This replay mode does NOT run physics, so deterministic is False.
        super().__init__(level, trajectory, physics=False)

        self.execution_speed = 1.0

        entities = cast(
            "List[Entity]",
            self.world_objects_controller.get_world_objects_by_type(Entity),
        )
        self.entity_map: Dict[str, "Entity"] = {
            obj.spawn_based_id: obj for obj in entities
        }

    def update(self, dt: float):
        dt *= self.execution_speed
        super().update(dt)

        if self.finished:
            return

        self.time_accumulator += dt

        while self.time_accumulator >= self.time_per_action:
            self.time_accumulator -= self.time_per_action
            self.current_step_index += 1
            if self.finished:
                self._apply_state(self.snapshots[-1])
                return

        prev_snapshot = self.snapshots[max(0, self.current_step_index - 1)]
        next_snapshot = self.snapshots[self.current_step_index]
        alpha = self.time_accumulator / self.time_per_action

        self._interpolate_and_apply_states(prev_snapshot, next_snapshot, alpha)

    def _interpolate_and_apply_states(
        self,
        prev_snapshot: "FrameSnapshot",
        next_snapshot: "FrameSnapshot",
        alpha: float,
    ):
        virtual_snapshot = interpolate_frame_snapshots(
            prev_snapshot, next_snapshot, alpha
        )
        self._apply_state(virtual_snapshot)

    def _apply_state(self, snapshot: "FrameSnapshot"):
        for entity_state in snapshot.entities:
            target_entity = self.entity_map.get(entity_state.entity_id)
            if target_entity:
                entity_state.apply_to_entity(target_entity)

    @property
    def finished(self) -> bool:
        return self.current_step_index >= len(self.snapshots)

    @property
    def snapshots(self) -> "List[FrameSnapshot]":
        return self.trajectory.frame_snapshots
