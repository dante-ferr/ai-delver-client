import cairosvg
from PIL import Image, ImageTk
import io
from pathlib import Path
import os
import re


class SvgImage(ImageTk.PhotoImage):
    def __init__(
        self,
        svg_path: str,
        stroke: str = "#000000",
        fill: str = "none",
        size: tuple[int, int] = (32, 32),
    ):
        png_data = self._process_svg(svg_path, stroke, fill, size)

        image = Image.open(io.BytesIO(png_data))
        super().__init__(image=image)

    def _process_svg(
        self, svg_path: str, stroke: str, fill: str, size: tuple[int, int]
    ):
        path = Path(svg_path)
        if not path.exists():
            raise FileNotFoundError(f"SVG file not found: {svg_path}")

        with open(svg_path, "r") as file:
            svg_content = file.read()

        svg_content = re.sub(r'stroke="[^"]+"', f'stroke="{stroke}"', svg_content)
        svg_content = re.sub(r'fill="[^"]+"', f'fill="{fill}"', svg_content)

        temp_svg_path = "temp_modified.svg"
        with open(temp_svg_path, "w") as temp_file:
            temp_file.write(svg_content)

        png_data = cairosvg.svg2png(
            url=temp_svg_path, output_width=size[0], output_height=size[1]
        )
        if not png_data:
            raise RuntimeError("Failed to convert SVG to PNG")

        os.remove(temp_svg_path)

        return png_data
