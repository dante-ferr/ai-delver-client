from bootstrap import *
import threading
import uvicorn
from api.server import app as api_app
from app_manager import app_manager


def run_api():
    uvicorn.run(api_app, host="0.0.0.0", port=8000, log_level="info")


def main():
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    app_manager.start_editor()  # Your main app logic


if __name__ == "__main__":
    main()
