import json


class Theme:
    def __init__(self, theme_name: str):
        self.path = "assets/themes/" + theme_name + ".json"

        with open(self.path, "r") as file:
            data = json.load(file)

        self.light_icon_color = data["CTkButton"]["text_color"][1]


default_theme = "orange"
theme = Theme(default_theme)
