from typing import Callable, Any

class AnimationEvent:
    event_sequence: Any
    event_index: int
    current_duration = 0.
    total_duration: float

    def __init__(self, event_sequence: Any, event_index=0, start_duration=0):
        self.event_sequence = event_sequence
        self.event_index = event_index
        self.total_duration = event_sequence[event_index]["duration"]
        self.current_duration = start_duration
    
    def update(self, frame_step: float, new_event_callback: Callable):
        """Update the animation event's duration and return the next event if the current event is finished."""
        self.current_duration += frame_step
        if self.current_duration >= self.total_duration:
            return new_event_callback(
                event_sequence=self.event_sequence,
                event_index=self._get_next_event_index(),
                start_duration=self.total_duration - self.current_duration
            )
        return None
    
    def _get_next_event_index(self):
        return self.event_index + 1 if self.event_index < len(self.event_sequence) - 1 else 0

    def _get_info_pair(self):
        return (
            self.event_sequence[self.event_index],
            self.event_sequence[self._get_next_event_index(self.event_index, self.event_sequence)]
        )