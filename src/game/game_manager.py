import threading
import time
from game.game import Game  # Ensure Game implements stop() correctly


class GameManager:
    def __init__(self):
        self.game_instance = None
        self.game_thread = None

    def start_game(self):
        """Starts a new game instance in a separate thread."""
        if self.game_instance:
            self.stop_game()
            time.sleep(0.5)  # Ensure the previous game closes before restarting

        self.game_thread = threading.Thread(target=self._run_game, daemon=True)
        self.game_thread.start()

    def _run_game(self):
        """Runs the game instance."""
        self.game_instance = Game()
        self.game_instance.run()

    def stop_game(self):
        """Stops the current game instance if it's running."""
        if self.game_instance:
            self.game_instance.stop()
            self.game_instance = None

    def restart_game(self):
        """Stops the current game and starts a new one."""
        self.stop_game()
        self.start_game()


game_manager = GameManager()
