from unittest import TestCase

from gamemaster.games import ElementRPSOptions, WinningRoundsSetting


class TestElementRPSOptions(TestCase):
    def setUp(self):
        self.use_hex_emojis = True
        self.round_setting = WinningRoundsSetting.THREE_ROUNDS
        self.element_rps_options = ElementRPSOptions(
            use_hex_emojis=self.use_hex_emojis,
            winning_rounds=self.round_setting
        )

    def test_initializes_properly(self):
        self.assertHasAttr(self.element_rps_options, "use_hex_emojis")
        self.assertEqual(self.element_rps_options.use_hex_emojis, self.use_hex_emojis)

        self.assertHasAttr(self.element_rps_options, "winning_rounds")
        self.assertEqual(self.element_rps_options.winning_rounds, self.round_setting)


    def test_initializes_with_default_values(self):
        default_hex_emojis = False
        default_round_setting = WinningRoundsSetting.TWO_ROUNDS

        element_rps_options = ElementRPSOptions.default()

        self.assertEqual(element_rps_options.use_hex_emojis, default_hex_emojis)
        self.assertEqual(element_rps_options.winning_rounds, default_round_setting)
