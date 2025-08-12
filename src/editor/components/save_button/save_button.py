from pathlib import Path
from editor.components import IconButton
from src.config import ASSETS_PATH
from editor.components.overlay.message_overlay import MessageOverlay


class SaveButton(IconButton):
    """Base class for save buttons that handle saving files with a confirmation dialog. This cannot be used directly and must be subclassed, because the _save method doesn't handle saving."""

    def __init__(self, parent, save_folder_path: str, file_type: str):
        super().__init__(parent, svg_path=str(ASSETS_PATH / "svg" / "save.svg"))
        if not save_folder_path:
            raise ValueError("Save folder path must be provided.")
        if not file_type:
            raise ValueError("File type must be provided.")

        self.file_type = file_type
        self.save_folder_path = Path(save_folder_path)

    def _on_click(self, event):
        file_path = self.save_folder_path / self.file_name
        if self.file_name == "":
            raise ValueError("File name must be defined in the subclass.")

        if file_path.is_dir():
            MessageOverlay(
                f"There is already a saved file with the same name as the current {self.file_type}. Do you want to overwrite it?",
                button_commands={
                    "Yes": self._save,
                    "No (cancel)": lambda: None,
                },
            )
        else:
            self._save()

    def _save(self):
        MessageOverlay(
            f"Sucessfully saved the {self.file_type}.",
            button_commands={
                "Ok": lambda: None,
            },
        )

    @property
    def file_name(self) -> str:
        """Returns the name of the file to save. OBS: this class must be overridden in subclasses."""
        return ""
