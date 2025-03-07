from typing import TYPE_CHECKING


class EntityRepresentation:
    def __init__(self, entity_name: str, position: tuple[float, float]):
        self.entity_name = entity_name
        self.position = position
