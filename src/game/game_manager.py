# game/game_manager.py
import threading
import time
import queue
from game.game import Game


class GameManager:
    def __init__(self):
        self.game_instance = None
        self.game_thread = None
        self._should_stop = False

        self.queue = queue.Queue()

    def start_game(self):
        """Starts a new game instance in a separate thread."""
        if self.game_instance:
            self.stop_game()
            time.sleep(0.5)  # Ensure previous game closes

        self._should_stop = False
        self.game_thread = threading.Thread(target=self._run_game, daemon=True)
        self.game_thread.start()

    def _run_game(self):
        """Runs the game instance."""
        self.game_instance = Game()
        self.game_instance.run()
        self.game_instance = None

    def stop_game(self):
        """Stops the current game instance if it's running."""
        if not self.game_instance:
            return

        self.game_instance.stop()

        if threading.current_thread() is not self.game_thread:
            if self.game_thread and self.game_thread.is_alive():
                self.game_thread.join()

        self.game_instance = None
        self.game_thread = None

    def restart_game(self):
        """Stops the current game and starts a new one."""
        self.stop_game()
        self.start_game()


game_manager = GameManager()
