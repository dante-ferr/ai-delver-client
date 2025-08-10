from bootstrap import *
from client_requests import send_training_request
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- Main Application Logic ---
async def main():
    """
    Main function to run the test client.
    It loads a level, sends a training request, and then listens for replay data.
    """
    level_path = "data/level_saves/test_1.dill"
    try:
        from level_loader import level_loader

        level_data = level_loader.load_level("data/level_saves/test_1.dill")

        # Request the ai server to train on this level
        await send_training_request(level_data)

    except FileNotFoundError:
        logging.error(f"Error: The level file '{level_path}' was not found.")
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main test script: {e}")


if __name__ == "__main__":
    asyncio.run(main())
