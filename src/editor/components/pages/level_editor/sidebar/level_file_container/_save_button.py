from editor.components.overlay.message_overlay import MessageOverlay
from editor.components import IconButton
from level_loader import level_loader


class SaveButton(IconButton):
    def __init__(self, parent):
        super().__init__(parent, svg_path="assets/svg/save.svg")

    def _on_click(self, event):
        if level_loader.level.same_name_saved:
            MessageOverlay(
                f"There is already a saved file with the same name as the current level ({level_loader.level.name}). Do you want to overwrite it?",
                button_commands={
                    "Yes": self._save,
                    "No (cancel)": lambda: None,
                },
            )
        else:
            self._save()

    def _save(self):
        level_loader.level.save()
        MessageOverlay(
            "Sucessfully saved the level.",
            button_commands={
                "Ok": lambda: None,
            },
        )
