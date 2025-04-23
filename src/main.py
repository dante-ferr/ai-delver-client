from bootstrap import *
from api import run_api
from app_manager import app_manager


def main():
    run_api()
    app_manager.start_editor()


if __name__ == "__main__":
    main()
