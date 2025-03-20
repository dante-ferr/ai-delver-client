from editor.level import level
import customtkinter as ctk
from editor.components import SvgImage
from editor.theme import theme


class LevelFileContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        ICON_SIZE = (20, 20)
        BUTTON_SIZE = (24, 24)

        save_icon = SvgImage(
            svg_path="assets/svg/save.svg",
            size=ICON_SIZE,
            fill=theme.icon_color,
        )
        save_button = ctk.CTkButton(
            self,
            text="",
            fg_color="transparent",
            width=BUTTON_SIZE[0],
            height=BUTTON_SIZE[1],
            hover_color="#555",
            image=save_icon.get_ctk_image(),
            command=self._save,
        )
        save_button.pack(side="left", padx=3.2, pady=0)

        load_icon = SvgImage(
            svg_path="assets/svg/load.svg",
            size=ICON_SIZE,
            fill=theme.icon_color,
        )
        load_button = ctk.CTkButton(
            self,
            text="",
            fg_color="transparent",
            width=BUTTON_SIZE[0],
            height=BUTTON_SIZE[1],
            hover_color="#555",
            image=load_icon.get_ctk_image(),
            command=self._load,
        )
        load_button.pack(padx=2, pady=0)

    def _save(self):
        level.save()

    def _load(self):
        # level.load()
        pass
