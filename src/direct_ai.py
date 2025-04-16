from bootstrap import *
import requests

if __name__ == "__main__":
    from level import level_loader

    level_loader.load_level("data/level_saves/My custom level.dill")
    # response = requests.post("http://localhost:8001/train")
    # print(response.json())

    while True:
        pass
