from runtime_view.game import Game
from typing import Optional
from editor import EditorApp
import logging
from level_loader import level_loader


class AppManager:
    def __init__(self):
        self._game = None
        self._editor: Optional[EditorApp] = None

    def start_game(self):
        if self._editor is not None:
            self._editor.withdraw()
        self._game = Game(level_loader.level)
        self._game.run()

        if self._editor is not None:
            self._editor.deiconify()

    def stop_game(self):
        if self._game is not None:
            self._game.stop()
            self._game = None

    def restart_game(self):
        self.stop_game()
        self.start_game()

    def start_editor(self):
        if self._editor is None:
            self._editor = EditorApp()
            logging.info("Starting editor")
            self._editor.mainloop()
        else:
            self._editor.deiconify()

    def stop_editor(self):
        if self._editor is not None:
            self._editor.withdraw()

    @property
    def editor_app(self):
        if self._editor is None:
            raise RuntimeError("Editor app not initialized")
        return self._editor


app_manager = AppManager()
