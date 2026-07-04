from unittest import TestCase
from unittest.mock import Mock

from discord.abc import User

from gamemaster.gamemaster import GameMaster
from gamemaster.games import ChubSweeperGame, ChubSweeperOptions
from gamemaster.models import Player


class TestChubSweeper(TestCase):
    def setUp(self):
        gamemaster_mock = Mock(GameMaster)

        self.host_id = 123456789
        user_mock = Mock(User, **{"id": self.host_id})
        self.dealer_mock = Mock(Player, **{"discord_user_id": self.host_id})

        chubsweeper_options_mock = Mock(ChubSweeperOptions)

        self.miners_amount = 5
        self.miners_mock = [Mock(Player) for _ in range(self.miners_amount)]

        self.chubsweeper_game = ChubSweeperGame(
            gamemaster_mock,
            user_mock,
            [self.dealer_mock, *self.miners_mock],
            options=chubsweeper_options_mock
        )


    def test_has_proper_title(self):
        chubsweeper_title = "ChubSweeper"
        self.assertEqual(self.chubsweeper_game.title_name(), chubsweeper_title)


    def test_has_proper_description(self):
        chubsweeper_description = ("Try to avoid landing on the ChubMines™, "
                                   "while appreciating the \"safes\".")
        self.assertEqual(self.chubsweeper_game.description(), chubsweeper_description)


    def test_has_proper_emojis(self):
        emojis = ["🤰🏻", "🫃🏻", "🫄🏻"]
        self.assertCountEqual(self.chubsweeper_game.emojis_collection(), emojis)


    def test_has_correct_amount_of_minimum_players(self):
        self.assertEqual(self.chubsweeper_game.minimum_players(), 2)


    def test_has_correct_amount_of_maximum_players(self):
        self.assertEqual(self.chubsweeper_game.maximum_players(), 9)


    def test_has_dealer(self):
        self.assertHasAttr(self.chubsweeper_game, "dealer")
        self.assertEqual(self.chubsweeper_game.dealer, self.dealer_mock)


    def test_has_miners(self):
        self.assertHasAttr(self.chubsweeper_game, "miners")
        self.assertCountEqual(self.chubsweeper_game.miners, self.miners_mock)


    def test_host_player_must_be_present(self):
        with self.assertRaises(ValueError):
            ChubSweeperGame(
                Mock(GameMaster),
                Mock(User, **{"id": 111111111111}),
                [Mock(Player) for _ in range(self.miners_amount)],
                options=Mock(ChubSweeperOptions)
            )
