from unittest import TestCase

from gamemaster.games import BlurLevel, ChubSweeperOptions


class TestChubSweeperOptions(TestCase):
    def setUp(self):
        self.private_mode = False
        self.fixed_width = 200
        self.fixed_height = 850
        self.blur_level_mock = BlurLevel.MILD
        self.amount_safes = 5
        self.amount_mines = 2
        self.chubsweeper_options = ChubSweeperOptions(
            private_mode=self.private_mode,
            fixed_width=self.fixed_width,
            fixed_height=self.fixed_height,
            blur_level=self.blur_level_mock,
            amount_safes=self.amount_safes,
            amount_mines=self.amount_mines
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

        self.assertHasAttr(self.chubsweeper_options, "amount_safes")
        self.assertEqual(self.chubsweeper_options.amount_safes, self.amount_safes)

        self.assertHasAttr(self.chubsweeper_options, "amount_mines")
        self.assertEqual(self.chubsweeper_options.amount_mines, self.amount_mines)


    def test_is_initialized_with_default_values(self):
        blur_level_default = BlurLevel.STRONG
        amount_safes_default = 3
        amount_mines_default = 1

        chubsweeper_options = ChubSweeperOptions.default()

        self.assertFalse(chubsweeper_options.private_mode)
        self.assertIsNone(chubsweeper_options.fixed_width)
        self.assertIsNone(chubsweeper_options.fixed_height)
        self.assertEqual(chubsweeper_options.blur_level, blur_level_default)
        self.assertEqual(chubsweeper_options.amount_safes, amount_safes_default)
        self.assertEqual(chubsweeper_options.amount_mines, amount_mines_default)
