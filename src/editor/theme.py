import json


class Theme:
    def __init__(self, theme_name: str):
        self.path = "assets/themes/" + theme_name + ".json"

        with open(self.path, "r") as file:
            data = json.load(file)

        self.icon_color = data["CTkLabel"]["text_color"][1]
        self.select_border_color = data["CTkButton"]["border_color"][1]


default_theme = "orange"
theme = Theme(default_theme)
