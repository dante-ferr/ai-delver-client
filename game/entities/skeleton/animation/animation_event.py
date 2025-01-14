from typing import Callable


class AnimationEvent:
    event_sequence: dict
    event_index: int
    current_duration = 0.0
    total_duration: float

    def __init__(self, event_sequence: dict, event_index=0, start_duration=0):
        self.event_sequence = event_sequence
        self.event_index = event_index
        # print("event_index: ", event_index)
        self.total_duration = event_sequence[event_index]["duration"]
        self.current_duration = start_duration

    def update(self, frame_step: float, new_event_callback: Callable):
        """Update the animation event's duration and return the next event if the current event is finished."""
        if self.current_duration >= self.total_duration:
            return new_event_callback(
                event_sequence=self.event_sequence,
                event_index=self._get_next_event_index(),
                start_duration=self.current_duration - self.total_duration,
            )
        self._execute_update_changes()
        self.current_duration += frame_step

        return None

    def _execute_update_changes(self):
        raise NotImplementedError

    def _get_next_event_index(self):
        # print("event_index: ", self.event_index + 1 if self.event_index < len(self.event_sequence) - 1 else 0)
        return (
            self.event_index + 1
            if self.event_index < len(self.event_sequence) - 1
            else 0
        )

    def _get_info_pair(self):
        return (
            self.event_sequence[self.event_index],
            self.event_sequence[self._get_next_event_index()],
        )
