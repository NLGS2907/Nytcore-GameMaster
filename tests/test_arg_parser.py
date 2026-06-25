from unittest import TestCase

from gamemaster.arg_parser import BotArgParser


class TestBotArgParser(TestCase):
    def setUp(self):
        self.parser = BotArgParser()


    def test_is_created_with_verbose_argument(self):
        self.assertIn('verbose', map(lambda action: action.dest, self.parser._actions))


    def test_is_created_with_only_bot_argument(self):
        self.assertIn('only_bot', map(lambda action: action.dest, self.parser._actions))