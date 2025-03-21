import customtkinter as ctk
from editor.components import SvgImage
from editor.theme import theme


class IconButton(ctk.CTkButton):
    def __init__(self, parent, svg_path: str):
        icon = SvgImage(
            svg_path=svg_path,
            size=(20, 20),
            fill=theme.icon_color,
        )

        super().__init__(
            parent,
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
