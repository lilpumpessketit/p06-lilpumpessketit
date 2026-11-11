from unittest import TestCase
from unittest.mock import MagicMock

from thumbor.transformer import Transformer


class ExtremeAspectCropTestCase(TestCase):
    def test_auto_crop_keeps_at_least_one_row_for_wide_target(self):
        engine = MagicMock()
        engine.size = (16, 16)

        transformer = Transformer(MagicMock())
        transformer.engine = engine
        transformer.target_width = 800.0
        transformer.target_height = 20.0
        transformer.get_center_of_mass = lambda: (8.0, 8.0)

        transformer.auto_crop()

        left, top, right, bottom = engine.crop.call_args[0]
        self.assertGreater(bottom - top, 0)
        self.assertGreater(right - left, 0)

    def test_fit_in_width_only_keeps_at_least_one_row(self):
        engine = MagicMock()
        engine.size = (940, 2)

        context = MagicMock()
        context.request.adaptive = False
        context.request.full = False
        context.request.width = 100
        context.request.height = 0

        transformer = Transformer(context)
        transformer.engine = engine
        transformer.target_width = 100.0
        transformer.target_height = 100.0 * 2 / 940

        transformer.fit_in_resize()

        width, height = engine.resize.call_args[0]
        self.assertGreaterEqual(height, 1)
        self.assertGreaterEqual(width, 1)

    def test_fit_in_width_only_zero_target_height_no_zero_division(self):
        engine = MagicMock()
        engine.size = (940, 2)

        context = MagicMock()
        context.request.adaptive = False
        context.request.full = False
        context.request.width = 100
        context.request.height = 0

        transformer = Transformer(context)
        transformer.engine = engine
        transformer.target_width = 100.0
        transformer.target_height = 0.0

        transformer.fit_in_resize()

        engine.resize.assert_called_once_with(100, 1)
