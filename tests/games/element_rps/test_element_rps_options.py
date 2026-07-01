from unittest import TestCase

from gamemaster.games import ElementRPSOptions, WinningRoundsSetting


class TestElementRPSOptions(TestCase):
    def setUp(self):
        self.use_hex_emojis = True
        self.round_setting = WinningRoundsSetting.THREE_ROUNDS
        self.round_timeout = 20
        self.element_rps_options = ElementRPSOptions(
            use_hex_emojis=self.use_hex_emojis,
            winning_rounds=self.round_setting,
            round_timeout=self.round_timeout
        )

    def test_initializes_properly(self):
        self.assertHasAttr(self.element_rps_options, "use_hex_emojis")
        self.assertEqual(self.element_rps_options.use_hex_emojis, self.use_hex_emojis)

        self.assertHasAttr(self.element_rps_options, "winning_rounds")
        self.assertEqual(self.element_rps_options.winning_rounds, self.round_setting)

        self.assertHasAttr(self.element_rps_options, "round_timeout")
        self.assertEqual(self.element_rps_options.round_timeout, self.round_timeout)


    def test_initializes_with_default_values(self):
        default_round_setting = WinningRoundsSetting.TWO_ROUNDS
        default_round_timeout = 30

        element_rps_options = ElementRPSOptions.default()

        self.assertFalse(element_rps_options.use_hex_emojis)
        self.assertEqual(element_rps_options.winning_rounds, default_round_setting)
        self.assertEqual(element_rps_options.round_timeout, default_round_timeout)
