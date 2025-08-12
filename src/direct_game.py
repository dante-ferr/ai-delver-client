from bootstrap import *
from app_manager import app_manager
from level.config import LEVEL_SAVE_FOLDER_PATH


if __name__ == "__main__":
    from level_loader import level_loader

    level_loader.load_level(f"{LEVEL_SAVE_FOLDER_PATH}/test_1")
    app_manager.start_game()
