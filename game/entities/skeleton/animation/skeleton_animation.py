from typing import Literal, Callable, TYPE_CHECKING, Type, Union, cast, TypedDict, Any
from .bone_event import BoneEvent, BoneEventType
from .slot_event import SlotEvent, SlotEventType
from ..bone import Bone
from ..slot import Slot

if TYPE_CHECKING:
    from ..skeleton import Skeleton

BoneEventsDict = dict[BoneEventType, list[BoneEvent]]
SlotEventsDict = dict[SlotEventType, list[SlotEvent]]
EventsDict = dict[Literal["bone", "slot"], BoneEventsDict | SlotEventsDict]

class SkeletonAnimation:
    duration: float
    frame = 0.
    speed: float

    events: EventsDict

    bone_info: Any
    slot_info: Any

    def __init__(self, info: Any, skeleton: "Skeleton", frame=0, speed=1.):
        self.duration = info["duration"]
        self.bone_info = info["bone"]
        self.slot_info = info["slot"]

        self.skeleton = skeleton
        self.speed = speed

        self._instantiate_events(frame)
    
    def set_frame(self, frame: float):
        self._instantiate_events(frame)
    
    def set_speed(self, speed: float):
        self.speed = speed
    
    def update(self, dt):
        frame_step = dt * self.speed

        def _update_part_events(self, Event: Type[Union[BoneEvent, SlotEvent]]):
            for event_type in Event.all_event_types:
                for event in self.events[event_type]:
                    new_event = event.update(frame_step, lambda part, event_sequence, event_index, start_duration: Event(
                        part,
                        event_sequence,
                        event_index,
                        start_duration
                    ))
                    if new_event:
                        self.events[Event.skeleton_part_type][event_type] = new_event
        
        _update_part_events(BoneEvent)
        _update_part_events(SlotEvent)

        self.frame += dt * self.speed

    def _instantiate_events(self, frame: float):
        self.events["bone"] = self._event_factory(
            info=self.bone_info,
            skeleton_parts=self.skeleton.bones,
            Event=BoneEvent,
            frame=frame
        )
        self.events["slot"] = self._event_factory(
            info=self.slot_info,
            skeleton_parts=self.skeleton.slots,
            Event=SlotEvent,
            frame=frame
        )

    def _event_factory(
        self,
        info: Any,
        skeleton_parts: dict[str, Bone] | dict[str, Slot],
        Event: Type[Union[BoneEvent, SlotEvent]],
        frame=0
    ):
        events: dict[str, list[Union[BoneEvent, SlotEvent]]] = {}
        
        event_types = Event.all_event_types
        for animation_info in info:
            part = skeleton_parts[animation_info["name"]]
            for event_type in event_types:
                if event_type in animation_info:
                    event_sequence = animation_info[event_type]
                    event_index, start_duration = self._frame_to_index_duration(frame, event_sequence)

                    events[event_type].append(Event(
                        part,
                        event_type=event_type,
                        event_sequence=event_sequence,
                        event_index=event_index,
                        start_duration=start_duration
                    ))
        
        return events

    def _frame_to_index_duration(self, frame_index: float, event_sequence: Any):
        """Convert a frame index to an event index and duration."""
        if frame_index > self.duration:
            raise ValueError("Frame index is greater than animation duration.")
        
        duration_count = 0
        i = 0

        for event in event_sequence:
            if duration_count >= frame_index:
                return i, duration_count - frame_index
            
            duration_count += event["duration"]
            i += 1
        
        raise ValueError("The animation does not contain the specified frame index. There may be a problem with the animation data.")