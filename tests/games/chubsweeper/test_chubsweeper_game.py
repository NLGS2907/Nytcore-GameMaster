from unittest import TestCase
from unittest.mock import Mock

from discord.abc import User

from gamemaster.gamemaster import GameMaster
from gamemaster.games import ChubSweeperGame, ChubSweeperOptions
from gamemaster.models import Player


class TestChubSweeper(TestCase):
    def setUp(self):
        gamemaster_mock = Mock(GameMaster)
        user_mock = Mock(User)
        chubsweeper_options_mock = Mock(ChubSweeperOptions)

        self.chubsweeper_game = ChubSweeperGame(
            gamemaster_mock,
            user_mock,
            [Mock(Player) for _ in range(5)],
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
