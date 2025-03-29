import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".."))

from editor import app
import queue
from game.game_manager import game_manager


def check_game_events():
    try:
        message = game_manager.queue.get_nowait()
        if message == "stop":
            game_manager.stop_game()
    except queue.Empty:
        pass
    app.after(100, check_game_events)


app.after(100, check_game_events)

app.mainloop()
