from pytiling import GridMap


class GameObjectsMap(GridMap):
    def __init__(self, size: tuple[int, int]):
        super().__init__(size)
