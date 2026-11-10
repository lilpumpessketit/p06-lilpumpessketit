from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine
from thumbor.ext.filters import _round_corner


def _white_rgba_png():
    buf = BytesIO()
    Image.new("RGBA", (300, 200), (255, 255, 255, 255)).save(buf, "PNG")
    return buf.getvalue()


def test_transparent_round_corner_edge_is_not_darkened():
    engine = Engine(Context(config=Config()))
    engine.load(_white_rgba_png(), ".png")
    width, height = engine.size

    # Same calls the round_corner filter makes with transparent set.
    engine.enable_alpha()
    mode, data = engine.image_data_as_rgb()
    imgdata = _round_corner.apply(
        1, mode, 60, 60, 255, 255, 255, width, height, data, True
    )
    engine.set_image_data(imgdata)

    image = engine.image.convert("RGBA")
    corner = image.crop((0, 0, 60, 60))
    for x in range(corner.width):
        for y in range(corner.height):
            r, g, b, a = corner.getpixel((x, y))
            if a > 0:
                assert min(r, g, b) >= 250, (
                    f"edge pixel at ({x},{y}) is darkened: "
                    f"rgba=({r},{g},{b},{a})"
                )
