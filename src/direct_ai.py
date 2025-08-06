from bootstrap import *
import requests
import logging
import dill
import base64

if __name__ == "__main__":
    from level_loader import level_loader

    level_loader.load_level("data/level_saves/test_1.dill")

    logging.info("Sending training request...")
    payload = {
        "level": base64.b64encode(dill.dumps(level_loader.level)).decode("ascii")
    }
    response = requests.post("http://localhost:8001/train", json=payload)
