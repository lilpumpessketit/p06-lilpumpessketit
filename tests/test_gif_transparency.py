import os
from io import BytesIO

from PIL import Image

from thumbor.config import Config
from thumbor.context import Context
from thumbor.engines.pil import Engine

STICKER = os.path.join(
    os.path.dirname(__file__), "..", "course", "images", "sticker.gif"
)


def test_resized_palette_gif_keeps_transparency_index():
    config = Config(
        PILLOW_PRESERVE_INDEXED_MODE=True, ALLOW_ANIMATED_GIFS=False
    )
    engine = Engine(Context(config=config))
    engine.extension = ".gif"

    with open(STICKER, "rb") as handle:
        buffer = handle.read()

    engine.image = engine.create_image(buffer)
    engine.resize(240, 160)
    output = engine.read(".gif")

    result = Image.open(BytesIO(output))
    assert "transparency" in result.info
