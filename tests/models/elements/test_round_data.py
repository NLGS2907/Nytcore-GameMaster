from unittest import TestCase

from gamemaster.models import ElementType, RPSRoundData, RPSRoundResult


class TestRPSRoundData(TestCase):
    def setUp(self):
        self.player_1_choice = ElementType.FIRE
        self.player_2_choice = ElementType.WATER
        self.round_result = RPSRoundResult.DEFEAT


    def test_has_proper_attributes(self):
        round_data = RPSRoundData(self.player_1_choice, self.player_2_choice, self.round_result)

        self.assertHasAttr(round_data, "player_1_choice")
        self.assertEqual(round_data.player_1_choice, self.player_1_choice)

        self.assertHasAttr(round_data, "player_2_choice")
        self.assertEqual(round_data.player_2_choice, self.player_2_choice)

        self.assertHasAttr(round_data, "result")
        self.assertEqual(round_data.result, self.round_result)
