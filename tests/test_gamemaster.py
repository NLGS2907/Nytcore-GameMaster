from unittest import TestCase

from discord import Intents, Permissions

from gamemaster.gamemaster import GameMaster

VERSION_LENGTH: int = 3

class TestGameMaster(TestCase):
    def setUp(self):
        self.gamemaster = GameMaster()

    def test_has_correct_version_format(self):
        ver = self.gamemaster.version()

        self.assertEqual(len(ver), VERSION_LENGTH)
        for v in ver:
            self.assertIsInstance(v, int)


    def test_has_all_intents(self):
        self.assertEqual(self.gamemaster.preferred_intents(), Intents.all())


    def test_has_correct_permissions(self):
        perms = Permissions.none()
        perms.update(
            view_channel=True,
            view_guild_insights=True,
            send_messages=True,
            create_public_threads=True,
            create_private_threads=True,
            send_messages_in_threads=True,
            manage_messages=True,
            pin_messages=True,
            manage_threads=True,
            embed_links=True,
            attach_files=True,
            read_message_history=True,
            use_external_emojis=True,
            use_external_stickers=True,
            add_reactions=True,
            use_application_commands=True,
            use_external_apps=True,
            create_polls=True
        )

        self.assertEqual(self.gamemaster.preferred_permissions(), perms)


    def test_is_created_with_verbose(self):
        gamemaster = GameMaster(verbose=True)

        self.assertTrue(gamemaster.verbose)


    def test_is_created_with_only_bot_logger(self):
        gamemaster = GameMaster(only_bot_logger=True)

        self.assertTrue(gamemaster.only_bot_logger)
