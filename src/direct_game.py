from bootstrap import *
from app_manager import app_manager

if __name__ == "__main__":
    from level_loader import level_loader

    level_loader.load_level("data/level_saves/test_1.dill")
    app_manager.start_game()
