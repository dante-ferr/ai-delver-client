import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".."))

from app_manager import app_manager


def main():
    ##
    app_manager.start_editor()

    ##
    # from level import level_loader

    # level_loader.load_level("data/level_saves/My custom level.dill")
    # app_manager.start_game()

    ##
    # from level import level_loader
    # from ai import train

    # level_loader.load_level("data/level_saves/My custom level.dill")
    # train()
    pass


if __name__ == "__main__":
    main()
