from unittest import TestCase

from gamemaster.models.player import Player, ProfileImgType

from ..helper import dummy_bmp


class TestPlayer(TestCase):
    def setUp(self):
        self.player_id = 0
        self.player_name = "John"
        self.player_discord_id = 12345678
        self.player = Player(self.player_id, self.player_name, self.player_discord_id, None, None)


    def test_has_attributes_properly_setup(self):
        self.assertHasAttr(self.player, "id")
        self.assertEqual(self.player.id, self.player_id)

        self.assertHasAttr(self.player, "username")
        self.assertEqual(self.player.username, self.player_name)

        self.assertHasAttr(self.player, "discord_user_id")
        self.assertEqual(self.player.discord_user_id, self.player_discord_id)

        self.assertHasAttr(self.player, "emoji")
        self.assertIsNone(self.player.emoji)

        self.assertHasAttr(self.player, "profile_img")
        self.assertIsNone(self.player.profile_img)

        self.assertHasAttr(self.player, "fav_color")
        self.assertIsNone(self.player.fav_color)

        self.assertIsNone(self.player.image_properties)


    def test_can_edit_the_username(self):
        new_username = "Jonathan"
        self.player.username = new_username

        self.assertEqual(self.player.username, new_username)


    def test_can_edit_emoji(self):
        new_emoji = "✅"
        self.player.emoji = new_emoji

        self.assertEqual(self.player.emoji, new_emoji)


    def test_can_edit_profile_image(self):
        size = 250
        new_img = dummy_bmp(size, size)
        self.player.profile_img = new_img
        img_props = self.player.image_properties

        self.assertIsNotNone(self.player.profile_img)
        self.assertIsInstance(self.player.profile_img, ProfileImgType)

        self.assertEqual(img_props.width, size)
        self.assertEqual(img_props.height, size)


    def test_can_edit_favourite_color(self):
        new_color = "#FA0E9C"
        self.player.fav_color = new_color

        self.assertEqual(self.player.fav_color, new_color)


    def test_should_throw_error_if_wrong_type_of_name(self):
        with self.assertRaises(TypeError):
            Player(0, 10, 1111111, None, None)


    def test_throw_error_if_empty_name(self):
        with self.assertRaises(ValueError):
            Player(0, "", 1111)


    def test_name_too_short(self):
        with self.assertRaises(ValueError):
            Player(0, "MJ", 1234)


    def test_name_too_long(self):
        with self.assertRaises(ValueError):
            Player(0, "ThisIsAVeryLongNmaeThatIsNotValidForThisContext", 1234)


    def test_default_emoji_is_None(self):
        player = Player(0, "abc", 2222)

        self.assertIsNone(player.emoji)


    def test_emoji_is_wrong_type(self):
        with self.assertRaises(TypeError):
            Player(0, "player", 12345678, emoji=[])


    def test_emoji_is_blank(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="")


    def test_emoji_has_more_than_one_char(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="\u2699\u2700")


    def test_text_is_not_emoji(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, emoji="A")


    def test_img_is_not_binary_file(self):
        with self.assertRaises(TypeError):
            Player(0, "player", 12345678, profile_img="Hello!")


    def test_img_is_too_small(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, profile_img=dummy_bmp(100, 100))


    def test_img_is_too_large(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, profile_img=dummy_bmp(1600, 1600))


    def test_img_not_square(self):
        width = 500
        height = 500

        player_with_wide_img = Player(0, "player", 12345678,
                                      profile_img=dummy_bmp(height * 2, height))
        player_with_tall_img = Player(0, "player", 12345678,
                                      profile_img=dummy_bmp(width, width * 2))


        wide_img_props = player_with_wide_img.image_properties
        self.assertEqual(wide_img_props.width, wide_img_props.height)
        self.assertEqual(wide_img_props.width, width)

        tall_img_props = player_with_tall_img.image_properties
        self.assertEqual(tall_img_props.width, tall_img_props.height)
        self.assertEqual(tall_img_props.height, height)


    def test_image_is_always_webp(self):
        player = Player(0, "player", 12345678, profile_img=dummy_bmp(500, 500))

        self.assertEqual(player.image_properties.format.upper(), "WEBP")


    def test_incorrect_color_type(self):
        with self.assertRaises(TypeError):
            Player(0, "player", 12345678, fav_color=123)


    def test_incorrect_color_format(self):
        with self.assertRaises(ValueError):
            Player(0, "player", 12345678, fav_color="abcdef")
