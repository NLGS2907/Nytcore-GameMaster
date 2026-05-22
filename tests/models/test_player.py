from unittest import TestCase

from gamemaster.models.player import Player


class TestPlayer(TestCase):
    def test_1_has_attributes_properly_setup(self):
        player_name = "John"
        player_discord_id = 12345678
        player = Player(0, player_name, player_discord_id, None, None)

        self.assertTrue(hasattr(player, "username"))
        self.assertEqual(player.username, player_name)

        self.assertTrue(hasattr(player, "discord_user_id"))
        self.assertEqual(player.discord_user_id, player_discord_id)

        self.assertTrue(hasattr(player, "emoji"))
        self.assertIsNone(player.emoji)

        self.assertTrue(hasattr(player, "profile_img"))
        self.assertIsNone(player.profile_img)


    def test_2_should_throw_error_if_wrong_type_of_name(self):
        with self.assertRaises(TypeError):
            Player(0, 10, 1111111, None, None)


    def test_3_throw_error_if_empty_name(self):
        with self.assertRaises(ValueError):
            Player(0, "", 1111)


    def test_4_name_too_short(self):
        with self.assertRaises(ValueError):
            Player(0, "MJ", 1234)


    def test_5_name_too_long(self):
        with self.assertRaises(ValueError):
            Player(0, "ThisIsAVeryLongNmaeThatIsNotValidForThisContext", 1234)


    def test_6_default_emoji_is_None(self):
        player = Player(0, "abc", 2222)

        self.assertIsNone(player.emoji)


    def test_7_emoji_is_wrong_type(self):
        with self.assertRaises(TypeError):
            Player(0, "player", 12345678, emoji=[])


    def test_8_emoji_is_blank(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="")


    def test_8_emoji_has_more_than_one_char(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="\u2699\u2700")


    def test_9_text_is_not_emoji(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="A")
