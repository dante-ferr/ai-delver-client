import customtkinter as ctk
from ..svg_image.svg_image import SvgImage
from app.theme import theme


class IconButton(ctk.CTkButton):

    def __init__(self, master, svg_path: str):
        icon = SvgImage(
            svg_path=svg_path,
            size=(20, 20),
            fill=theme.icon_color,
        )

        super().__init__(
            master,
            text="",
            fg_color="transparent",
            width=24,
            height=24,
            hover_color="#555",
            image=icon.get_ctk_image(),
        )

        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        pass
