from unittest import TestCase

from gamemaster.games import WinningRoundsSetting


class TestWinningRoundsSetting(TestCase):
    def test_is_initialized_properly(self):
        self.assertHasAttr(WinningRoundsSetting, "ONE_ROUND")
        self.assertEqual(WinningRoundsSetting.ONE_ROUND, 1)

        self.assertHasAttr(WinningRoundsSetting, "TWO_ROUNDS")
        self.assertEqual(WinningRoundsSetting.TWO_ROUNDS, 2)

        self.assertHasAttr(WinningRoundsSetting, "THREE_ROUNDS")
        self.assertEqual(WinningRoundsSetting.THREE_ROUNDS, 3)

        self.assertHasAttr(WinningRoundsSetting, "FOUR_ROUNDS")
        self.assertEqual(WinningRoundsSetting.FOUR_ROUNDS, 4)

        self.assertHasAttr(WinningRoundsSetting, "FIVE_ROUNDS")
        self.assertEqual(WinningRoundsSetting.FIVE_ROUNDS, 5)

