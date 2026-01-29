from level_loader import level_loader
from editor.components import TitleTextbox


class LevelTitleTextbox(TitleTextbox):

    def __init__(self, master):
        super().__init__(master, level_loader.level.name)

    def _update_name(self, event=None):
        level_loader.level.name = self._get_input()
