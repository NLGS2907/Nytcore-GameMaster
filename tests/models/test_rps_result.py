from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from gamemaster.models import ElementType, Player, RPSResult, RPSRoundData, RPSRoundResult


class TestRPSResult(TestCase):
    def setUp(self):
        self.game_id = 10
        self.player_1_mock = Mock(Player, **{
            "id": 1,
            "username": "Billy",
            "discord_user_id": 123456789,
            "emoji": None
        })
        self.player_2_mock = Mock(Player, **{
            "id": 2,
            "username": "Thomas",
            "discord_user_id": 987654321,
            "emoji": "✅"
        })
        self.saved_at = datetime(2026, 12, 11, 23, 42, 56)

        self.rps_result = RPSResult(self.game_id,
                                    self.player_1_mock, self.player_2_mock,
                                    [], self.saved_at)


    def test_initializes_with_attributes(self):
        self.assertHasAttr(self.rps_result, "id")
        self.assertEqual(self.rps_result.id, self.game_id)

        self.assertHasAttr(self.rps_result, "player_1")
        self.assertEqual(self.rps_result.player_1, self.player_1_mock)

        self.assertHasAttr(self.rps_result, "player_2")
        self.assertEqual(self.rps_result.player_2, self.player_2_mock)

        self.assertHasAttr(self.rps_result, "rounds")
        self.assertFalse(self.rps_result.rounds) # is it empty?

        self.assertHasAttr(self.rps_result, "saved_at")
        self.assertEqual(self.rps_result.saved_at, self.saved_at)


    def test_can_edit_player_1(self):
        new_player = Mock(Player)

        self.rps_result.player_1 = new_player

        self.assertEqual(self.rps_result.player_1, new_player)


    def test_can_edit_player_2(self):
        new_player = Mock(Player)

        self.rps_result.player_2 = new_player

        self.assertEqual(self.rps_result.player_2, new_player)


    def test_can_edit_rounds_list(self):
        new_rounds = [Mock(RPSRoundData), Mock(RPSRoundData), Mock(RPSRoundData)]

        self.rps_result.rounds = new_rounds

        self.assertEqual(self.rps_result.rounds, new_rounds)


    def test_can_edit_saving_date(self):
        new_save_date = datetime(2015, 8, 17, 0, 1, 13)

        self.rps_result.saved_at = new_save_date

        self.assertEqual(self.rps_result.saved_at, new_save_date)


    def test_can_add_rounds(self):
        self.assertEqual(self.rps_result.how_many_rounds(), 0)

        self.rps_result.add_data(ElementType.WIND, ElementType.WATER, RPSRoundResult.TIE)

        self.assertEqual(self.rps_result.how_many_rounds(), 1)
        self.assertEqual(self.rps_result.last_round(), Mock(RPSRoundData, **{
            "player_1_choice": ElementType.WIND,
            "player_2_choice": ElementType.WATER,
            "result": RPSRoundResult.TIE
        }))


    def test_can_retrieve_last_round(self):
        last_round = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.FIRE,
            "player_2_choice": ElementType.WATER,
            "result": RPSRoundResult.DEFEAT
        })
        rounds = [Mock(RPSRoundData), Mock(RPSRoundData), Mock(RPSRoundData), last_round]

        self.assertIsNone(self.rps_result.last_round())
        self.rps_result.rounds = rounds

        self.assertEqual(self.rps_result.how_many_rounds(), len(rounds))
        self.assertEqual(self.rps_result.last_round(), last_round)


    def test_can_determine_when_player_1_wins(self):
        round_data = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.IRON,
            "player_2_choice": ElementType.ELECTRIC,
            "result": RPSRoundResult.VICTORY,
        })

        self.assertEqual(self.rps_result.determine_winner(round_data), self.player_1_mock)


    def test_can_determine_when_player_2_wins(self):
        round_data = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.WATER,
            "player_2_choice": ElementType.ELECTRIC,
            "result": RPSRoundResult.DEFEAT,
        })

        self.assertEqual(self.rps_result.determine_winner(round_data), self.player_2_mock)


    def test_can_determine_when_players_tie(self):
        round_data = Mock(RPSRoundData, **{
            "player_1_choice": ElementType.IRON,
            "player_2_choice": ElementType.IRON,
            "result": RPSRoundResult.TIE,
        })

        self.assertIsNone(self.rps_result.determine_winner(round_data))


    def test_can_yield_from_rounds(self):
        rounds = [
            Mock(RPSRoundData, **{
                "player_1_choice": ElementType.IRON,
                "player_2_choice": ElementType.IRON,
                "result": RPSRoundResult.TIE,
            }),
            Mock(RPSRoundData, **{
                "player_1_choice": ElementType.WATER,
                "player_2_choice": ElementType.IRON,
                "result": RPSRoundResult.TIE,
            }),
            Mock(RPSRoundData, **{
                "player_1_choice": ElementType.IRON,
                "player_2_choice": ElementType.WIND,
                "result": RPSRoundResult.DEFEAT,
            })
        ],
        self.rps_result.rounds = rounds

        for i, round in enumerate(self.rps_result.walk_rounds()):
            with self.subTest(index=i, cur_round=round):
                self.assertEqual(round, rounds[i])


    def test_can_detect_last_two_null_rounds(self):
        rounds = [
            Mock(RPSRoundData, **{"choices_are_null.return_value": False}),
            Mock(RPSRoundData, **{"choices_are_null.return_value": True}),
            Mock(RPSRoundData, **{"choices_are_null.return_value": True})
        ]
        self.rps_result.rounds = rounds

        self.assertFalse(self.rps_result.last_null_rounds(3))
        self.assertTrue(self.rps_result.last_null_rounds(2))


    def test_last_rounds_null_with_invalid_value(self):
        rounds = [
            Mock(RPSRoundData, **{"choices_are_null.return_value": False}),
            Mock(RPSRoundData, **{"choices_are_null.return_value": False}),
            Mock(RPSRoundData, **{"choices_are_null.return_value": True})
        ]
        self.rps_result.rounds = rounds

        self.assertFalse(self.rps_result.last_null_rounds(0))
        self.assertFalse(self.rps_result.last_null_rounds(-1))
        self.assertFalse(self.rps_result.last_null_rounds(10))
