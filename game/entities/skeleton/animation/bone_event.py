from typing import Literal, Callable, Any
from .animation_event import AnimationEvent
from ..bone import Bone

BoneEventType = Literal["translateFrame", "rotateFrame", "scaleFrame"]

class BoneEvent(AnimationEvent):
    skeleton_part_type = "bone"
    bone: Bone
    all_event_types: list[BoneEventType] = ["translateFrame", "rotateFrame", "scaleFrame"]
    event_type: BoneEventType

    def __init__(self, bone: Bone, event_type: BoneEventType, event_sequence: Any, event_index=0, start_duration=0):
        super().__init__(event_sequence, event_index, start_duration)
        self.bone = bone
        self.event_type = event_type
    
    def update(self, frame_step: float, new_event_callback: Callable):
        info = self._get_info_pair()

        if self.event_type == "translateFrame":
            x = info[0]["x"] + (info[2]["x"] - info[0]["x"]) * self.current_duration / self.total_duration
            y = info[0]["y"] + (info[2]["y"] - info[0]["y"]) * self.current_duration / self.total_duration
            self.bone.set_position(x, y)
        elif self.event_type == "rotateFrame":
            angle = info[0]["rotate"] + (info[2]["rotate"] - info[0]["rotate"]) * self.current_duration / self.total_duration
            self.bone.set_angle(angle)
        elif self.event_type == "scaleFrame":
            x = info[0]["x"] + (info[2]["x"] - info[0]["x"]) * self.current_duration / self.total_duration
            y = info[0]["y"] + (info[2]["y"] - info[0]["y"]) * self.current_duration / self.total_duration
            self.bone.set_scale(x, y)

        return super().update(frame_step, lambda event_sequence, event_index, start_duration: 
            new_event_callback(self.bone, event_sequence, event_index, start_duration)
        )