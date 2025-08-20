from .level_selector import LevelSelector
from .canvas_objects import CanvasObjectsManager


class CanvasController:
    def __init__(self):
        self.level_selector = LevelSelector()
        self.objects_manager = CanvasObjectsManager()


canvas_controller = CanvasController()
