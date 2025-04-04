from .item import Item


class Goal(Item):
    def __init__(self, variation: str):
        super().__init__(f"assets/img/representations/goal/{variation}.png")
