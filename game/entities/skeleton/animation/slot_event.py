from typing import Literal, Callable, Any
from .animation_event import AnimationEvent
from ..slot import Slot

SlotEventType = Literal["displayFrame"]

class SlotEvent(AnimationEvent):
    skeleton_part_type = "slot"
    slot: Slot
    all_event_types: list[SlotEventType] = ["displayFrame"]
    event_type: SlotEventType

    def __init__(self, slot: Slot, event_type: SlotEventType, event_sequence: Any, event_index=0, start_duration=0):
        super().__init__(event_sequence, event_index, start_duration)
        self.slot = slot
        self.event_type = event_type
    
    def update(self, frame_step: float, new_event_callback: Callable):
        info = self._get_info_pair()

        if self.event_type == "displayFrame":
            display_index = info[0]["value"]
            self.slot.change_display(display_index)

        return super().update(frame_step, lambda event_sequence, event_index, start_duration: 
            new_event_callback(self.slot, event_sequence, event_index, start_duration)
        )