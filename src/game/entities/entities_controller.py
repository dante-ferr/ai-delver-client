from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import Entity


class EntitiesController:
    def __init__(self):
        self.entities: set["Entity"] = set()
        self.entity_groups: dict[str, set["Entity"]] = {}

    def add_entity(
        self,
        entity: "Entity",
        group_name: str | None = None,
        unique_identifier: str | None = None,
    ):
        self.entities.add(entity)

        if group_name is not None:
            if group_name not in self.entity_groups.keys():
                self.entity_groups[group_name] = set()
            self.entity_groups[group_name].add(entity)

        if unique_identifier is not None:
            setattr(self, unique_identifier, entity)

    def get_entity_by_name(self, name: str):
        return getattr(self, name)

    def update_entities(self, dt: float):
        for entity in self.entities:
            entity.update(dt)
