from io import BytesIO
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock

from discord.abc import User

from gamemaster.embeds import ProfileEmbed
from gamemaster.gamemaster import GameMaster
from gamemaster.models import Player


class TestProfileEmbed(IsolatedAsyncioTestCase):
    def setUp(self):
        self.gamemaster_mock = Mock(GameMaster, **{
            "fetch_avatar.return_value": BytesIO()
        })
        self.player_mock = Mock(Player, **{
            "username": "Chad",
            "fav_color": None,
            "profile_img": None,
            "image_properties": None
        })
        self.user_mock = Mock(User)

        self.profile_embed = ProfileEmbed(self.gamemaster_mock, self.player_mock, self.user_mock)


    def test_is_initialized_properly(self):
        self.assertHasAttr(self.profile_embed, 'bot')
        self.assertEqual(self.profile_embed.bot, self.gamemaster_mock)

        self.assertHasAttr(self.profile_embed, 'player')
        self.assertEqual(self.profile_embed.player, self.player_mock)

        self.assertHasAttr(self.profile_embed, 'discord_user')
        self.assertEqual(self.profile_embed.discord_user, self.user_mock)

        self.assertHasAttr(self.profile_embed, 'thumbnail_file')
        self.assertIsNone(self.profile_embed.thumbnail_file)


    async def test_can_prepare_embed(self):
        await self.profile_embed.prepare()

        self.assertIsNotNone(self.profile_embed.thumbnail_file)
