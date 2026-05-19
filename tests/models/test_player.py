from unittest import TestCase

from gamemaster.models.player import Player


class TestPlayer(TestCase):
    def test_1_has_attributes_properly_setup(self):
        player_name = "John"
        player_discord_id = 12345678
        player = Player(player_name, player_discord_id, None, None)

        self.assertTrue(hasattr(player, "username"))
        self.assertEqual(player.username, player_name)

        self.assertTrue(hasattr(player, "discord_user_id"))
        self.assertEqual(player.discord_user_id, player_discord_id)

        self.assertTrue(hasattr(player, "emoji"))
        self.assertIsNone(player.emoji)

        self.assertTrue(hasattr(player, "profile_img"))
        self.assertIsNone(player.profile_img)
