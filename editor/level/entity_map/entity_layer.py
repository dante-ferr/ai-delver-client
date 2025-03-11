from .entity_representation import EntityRepresentation


class EntityLayer:
    def __init__(self, name: str):
        self.name = name
        self.size: tuple[float, float] = (0, 0)
        self.entity_representations: dict[
            tuple[float, float], "EntityRepresentation"
        ] = {}
