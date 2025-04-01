import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".."))

from app_manager import app_manager


def main():
    app_manager.start_editor()


if __name__ == "__main__":
    main()
