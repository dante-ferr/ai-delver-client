from bootstrap import *
from app_manager import app_manager

if __name__ == "__main__":
    from level import level_loader

    level_loader.load_level("data/level_saves/My custom level.dill")
    app_manager.start_game()
