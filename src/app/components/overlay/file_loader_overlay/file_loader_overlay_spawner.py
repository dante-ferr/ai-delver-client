from pathlib import Path
from app.components.overlay.file_loader_overlay import FileLoaderOverlay
from app.components.overlay.message_overlay import MessageOverlay
import inflect

p = inflect.engine()


class FileLoaderOverlaySpawner:
    def __init__(
        self,
        file_path: str | Path,
        file_type: str,
        overlay_class: type[FileLoaderOverlay] = FileLoaderOverlay,
    ):
        file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        self.file_type = file_type

        file_dirs: dict[str, Path] = {}

        if not file_path.exists():
            self._empty_folder_error()
            return

        for file_dir in [
            file_dir for file_dir in file_path.iterdir() if file_dir.is_dir()
        ]:
            file_dirs[file_dir.name] = file_dir

        if not file_dirs:
            self._empty_folder_error()
            return

        overlay_class(file_dirs, file_type)

    def _empty_folder_error(self):
        MessageOverlay(
            f"The folder storing {p.plural(self.file_type)} is empty.",
            subject="Error",
        )
