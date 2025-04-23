from bootstrap import *
import requests
import logging

if __name__ == "__main__":
    from level import level_loader

    level_loader.load_level("data/level_saves/My custom level.dill")

    from api import run_api, api_ready

    run_api()

    api_ready.wait()

    logging.info("Sending training request...")
    response = requests.post("http://localhost:8001/train")
