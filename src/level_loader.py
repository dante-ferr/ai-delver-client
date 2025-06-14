from level import LevelLoader
import json

with open("src/config.json", "r") as f:
    config = json.load(f)

save_folder_path = config["save_folder_path"]
level_loader = LevelLoader(save_folder_path=save_folder_path)
