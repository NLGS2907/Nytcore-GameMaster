from unittest import TestCase

from gamemaster.games import BlurLevel, ChubSweeperOptions


class TestChubSweeperOptions(TestCase):
    def setUp(self):
        self.private_mode = False
        self.fixed_width = 200
        self.fixed_height = 850
        self.blur_level_mock = BlurLevel.MILD
        self.chubsweeper_options = ChubSweeperOptions(
            private_mode=self.private_mode,
            fixed_width=self.fixed_width,
            fixed_height=self.fixed_height,
            blur_level=self.blur_level_mock
        )


    def test_is_initialized_properly(self):
        self.assertHasAttr(self.chubsweeper_options, "private_mode")
        self.assertEqual(self.chubsweeper_options.private_mode, self.private_mode)

        self.assertHasAttr(self.chubsweeper_options, "fixed_width")
        self.assertEqual(self.chubsweeper_options.fixed_width, self.fixed_width)

        self.assertHasAttr(self.chubsweeper_options, "fixed_height")
        self.assertEqual(self.chubsweeper_options.fixed_height, self.fixed_height)

        self.assertHasAttr(self.chubsweeper_options, "blur_level")
        self.assertEqual(self.chubsweeper_options.blur_level, self.blur_level_mock)


    def test_is_initialized_with_default_values(self):
        blur_level_default = BlurLevel.STRONG

        chubsweeper_options = ChubSweeperOptions.default()

        self.assertFalse(chubsweeper_options.private_mode)
        self.assertIsNone(chubsweeper_options.fixed_width)
        self.assertIsNone(chubsweeper_options.fixed_height)
        self.assertEqual(chubsweeper_options.blur_level, blur_level_default)
