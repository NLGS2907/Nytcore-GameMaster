from unittest import TestCase
from unittest.mock import Mock

from discord.abc import User

from gamemaster.gamemaster import GameMaster
from gamemaster.games import ElementRPSGame, ElementRPSOptions, RPSRoundResult, WinningRoundsSetting
from gamemaster.models import ElementType, Player
from gamemaster.repositories import RepositoryConfiguration, RPSResultRepository


class TestElementRPSGame(TestCase):
    def setUp(self):
        self.rps_result_repo_mock = Mock(RPSResultRepository)
        gamemaster_mock = Mock(GameMaster, **{
            "repositories": Mock(RepositoryConfiguration, **{
                "rps_result": self.rps_result_repo_mock
            })
        })
        user_mock = Mock(User)
        self.player_1_mock = Mock(Player)
        self.player_2_mock = Mock(Player)

        self.max_rounds = WinningRoundsSetting.TWO_ROUNDS
        rps_options_mock = Mock(ElementRPSOptions, **{
            "winning_rounds": self.max_rounds
        })

        self.element_rps_game = ElementRPSGame(
            gamemaster_mock,
            user_mock,
            [self.player_1_mock, self.player_2_mock],
            options=rps_options_mock
        )


    def test_initializes_with_players(self):
        self.assertHasAttr(self.element_rps_game, "player_1")
        self.assertEqual(self.element_rps_game.player_1, self.player_1_mock)

        self.assertHasAttr(self.element_rps_game, "player_2")
        self.assertEqual(self.element_rps_game.player_2, self.player_2_mock)


    def test_starts_with_empty_rounds(self):
        self.assertEqual(self.element_rps_game.current_round, 0)
        self.assertFalse(self.element_rps_game.round_finished)


    def test_starts_with_empty_choices(self):
        player_1_choice, player_2_choice = self.element_rps_game.get_choices()

        self.assertIsNone(player_1_choice)
        self.assertIsNone(player_2_choice)


    def test_has_proper_title(self):
        game_title = "Element Rock-Paper-Scissors"
        self.assertEqual(self.element_rps_game.title_name(), game_title)


    def test_has_proper_description(self):
        game_description = "Classic game of Rock-Paper-Scissors, but with NIKKE's element codes!"
        self.assertEqual(self.element_rps_game.description(), game_description)


    def test_has_proper_emojis(self):
        wind_emoji = "💨"
        water_emoji = "💦"
        iron_emoji = "🔩"
        fire_emoji = "🔥"
        electric_emoji = "⚡"

        self.assertEqual(self.element_rps_game.wind_emoji(), wind_emoji)
        self.assertEqual(self.element_rps_game.water_emoji(), water_emoji)
        self.assertEqual(self.element_rps_game.iron_emoji(), iron_emoji)
        self.assertEqual(self.element_rps_game.fire_emoji(), fire_emoji)
        self.assertEqual(self.element_rps_game.electric_emoji(), electric_emoji)

        self.assertCountEqual(self.element_rps_game.emojis_collection(),
                              [wind_emoji, water_emoji, iron_emoji, fire_emoji, electric_emoji])


    def test_has_correct_amount_of_minimum_players(self):
        self.assertEqual(self.element_rps_game.minimum_players(), 2)


    def test_has_correct_amount_of_maximum_players(self):
        self.assertEqual(self.element_rps_game.maximum_players(), 2)


    def test_can_make_choices_for_player_1(self):
        expected_choice = ElementType.WIND

        self.element_rps_game.make_choice(expected_choice, True)
        player_1_choice, _ = self.element_rps_game.get_choices()

        self.assertTrue(self.element_rps_game.has_made_choice(True))
        self.assertEqual(player_1_choice, expected_choice)


    def test_can_make_choices_for_player_2(self):
        expected_choice = ElementType.ELECTRIC

        self.element_rps_game.make_choice(expected_choice, False)
        _, player_2_choice = self.element_rps_game.get_choices()

        self.assertTrue(self.element_rps_game.has_made_choice(False))
        self.assertEqual(player_2_choice, expected_choice)


    def test_know_when_both_players_have_chosen(self):
        self.assertFalse(self.element_rps_game.choices_made())

        self.element_rps_game.make_choice(ElementType.ELECTRIC, True)
        self.assertFalse(self.element_rps_game.choices_made())

        self.element_rps_game.make_choice(ElementType.FIRE, False)
        self.assertTrue(self.element_rps_game.choices_made())


    def test_can_reset_choices(self):
        self.element_rps_game.make_choice(ElementType.ELECTRIC, True)
        self.element_rps_game.make_choice(ElementType.ELECTRIC, False)
        choice_1, choice_2 = self.element_rps_game.get_choices()

        self.assertIsNotNone(choice_1)
        self.assertIsNotNone(choice_2)

        self.element_rps_game.reset_choices()
        reset_choice_1, reset_choice_2 = self.element_rps_game.get_choices()

        self.assertIsNone(reset_choice_1)
        self.assertIsNone(reset_choice_2)


    def _assert_weakness(self, element: ElementType, weakness: ElementType):
        self.assertTrue(self.element_rps_game.weak_against(element, weakness))


    def test_can_process_weaknesses(self):
        self._assert_weakness(ElementType.WIND, ElementType.FIRE)
        self._assert_weakness(ElementType.IRON, ElementType.WIND)
        self._assert_weakness(ElementType.ELECTRIC, ElementType.IRON)
        self._assert_weakness(ElementType.WATER, ElementType.ELECTRIC)
        self._assert_weakness(ElementType.FIRE, ElementType.WATER)


    def test_no_choice_is_weak_against_everything(self):
        for element in ElementType:
            with self.subTest(element=element):
                self._assert_weakness(None, element)


    def test_if_both_choices_are_null_then_its_a_tie(self):
        self.assertFalse(self.element_rps_game.weak_against(None, None))


    def _play_round(self, player_1_choice: ElementType, player_2_choice: ElementType):
        self.element_rps_game.make_choice(player_1_choice, True)
        self.element_rps_game.make_choice(player_2_choice, False)
        self.element_rps_game.resolve()


    def _play_round_and_reset(self, player_1_choice: ElementType, player_2_choice: ElementType):
        self._play_round(player_1_choice, player_2_choice)
        self.element_rps_game.reset_round()


    def _assert_resolved_round(self,
                               player_1_choice: ElementType,
                               player_2_choice: ElementType,
                               expected_round_result: RPSRoundResult,
                               expected_winner: Player):
        self._play_round(player_1_choice, player_2_choice)

        self.assertTrue(self.element_rps_game.round_finished)
        last_round_data = self.element_rps_game.last_record()

        self.assertIsNotNone(last_round_data)
        self.assertEqual(last_round_data.player_1_choice, player_1_choice)
        self.assertEqual(last_round_data.player_2_choice, player_2_choice)
        self.assertEqual(last_round_data.result, expected_round_result)
        self.assertEqual(self.element_rps_game.determine_winner(last_round_data), expected_winner)


    def test_can_resolve_a_tying_round(self):
        self._assert_resolved_round(ElementType.IRON, ElementType.IRON, RPSRoundResult.TIE, None)


    def test_can_resolve_a_winning_round(self):
        self._assert_resolved_round(ElementType.WATER, ElementType.FIRE,
                                    RPSRoundResult.VICTORY, self.player_1_mock)


    def test_can_resolve_a_losing_round(self):
        self._assert_resolved_round(ElementType.WIND, ElementType.FIRE,
                                    RPSRoundResult.DEFEAT, self.player_2_mock)


    def test_can_reset_the_round(self):
        current_round = self.element_rps_game.current_round
        self._play_round_and_reset(ElementType.ELECTRIC, ElementType.WATER)
        choice_1, choice_2 = self.element_rps_game.get_choices()

        self.assertEqual(self.element_rps_game.current_round, current_round + 1)
        self.assertFalse(self.element_rps_game.round_finished)
        self.assertIsNone(choice_1)
        self.assertIsNone(choice_2)


    def test_can_process_the_scores(self):
        self._play_round_and_reset(ElementType.WATER, ElementType.FIRE)
        self._play_round_and_reset(ElementType.IRON, ElementType.IRON)
        self._play_round_and_reset(ElementType.IRON, ElementType.ELECTRIC)
        self._play_round_and_reset(ElementType.IRON, ElementType.WIND)

        player_1_score, player_2_score = self.element_rps_game.get_scores()

        self.assertEqual(player_1_score, 2)
        self.assertEqual(player_2_score, 1)


    def _play_until_finished(self, is_player_1: bool):
        player_1_choice = (ElementType.WIND if is_player_1 else ElementType.ELECTRIC)
        for _ in range(self.max_rounds):
            self._play_round(player_1_choice, ElementType.IRON)


    def _assert_player_has_enough_score(self, is_player_1: bool):
        self.assertFalse(self.element_rps_game.enough_points(is_player_1))

        self._play_until_finished(is_player_1)

        self.assertTrue(self.element_rps_game.enough_points(is_player_1))


    def test_knows_when_player_1_has_enough_points(self):
        self._assert_player_has_enough_score(True)


    def test_knows_when_player_2_has_enough_points(self):
        self._assert_player_has_enough_score(False)


    def test_detects_when_player_1_wins_the_game(self):
        self.assertIsNone(self.element_rps_game.finished())

        self._play_until_finished(True)

        self.assertEqual(self.element_rps_game.finished(), self.player_1_mock)


    def test_detects_when_player_2_wins_the_game(self):
        self.assertIsNone(self.element_rps_game.finished())

        self._play_until_finished(False)

        self.assertEqual(self.element_rps_game.finished(), self.player_2_mock)


    def test_can_process_stats(self):
        self._play_round(ElementType.WIND, ElementType.WIND)
        self._play_round(ElementType.WIND, ElementType.WATER)
        self._play_round(ElementType.WIND, ElementType.IRON)
        self._play_round(ElementType.ELECTRIC, ElementType.IRON)
        self._play_round(ElementType.FIRE, ElementType.WIND)

        rps_stats = self.element_rps_game.process_stats()

        self.assertEqual(rps_stats.ties_count, 2)
        self.assertCountEqual(rps_stats.player_1_favs, [ElementType.WIND])
        self.assertCountEqual(rps_stats.player_2_favs, [ElementType.WIND, ElementType.IRON])


    def test_saves_the_games(self):
        self._play_until_finished(True)

        self.element_rps_game.save()

        self.rps_result_repo_mock.save.assert_called_once()
