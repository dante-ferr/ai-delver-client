from pytiling import GridElement


class WorldObjectRepresentation(GridElement):
    """A representation of a world object (parent of game entities). Its name should be the same as the canvas object that represents it"""

    def __init__(self, position: tuple[int, int], name: str, **args):
        super().__init__(position, name, **args)
