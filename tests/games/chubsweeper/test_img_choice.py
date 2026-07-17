from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock

from gamemaster.games import ImageChoice, ImagePairHolder


class TestImageChoice(TestCase):
    def setUp(self):
        self.base = Mock(BytesIO)
        self.blurred = Mock(BytesIO)
        holder = Mock(ImagePairHolder, **{
            "base": self.base,
            "blurred_copy_with_number.return_value": self.blurred
        })
        self.is_mine = True
        self.num = 8

        self.img_choice = ImageChoice(holder, self.is_mine, self.num)


    def test_is_initialized_properly(self):
        self.assertHasAttr(self.img_choice, "mine")
        self.assertEqual(self.img_choice.mine, self.is_mine)

        self.assertHasAttr(self.img_choice, "uncovered")
        self.assertFalse(self.img_choice.uncovered)

        self.assertHasAttr(self.img_choice, "number")
        self.assertEqual(self.img_choice.number, self.num)


    def test_generates_a_blurred_copy(self):
        self.assertIsInstance(self.img_choice.numbered_blurred, BytesIO)


    def test_can_uncover_choice(self):
        is_mine = self.img_choice.uncover()

        self.assertEqual(self.img_choice.mine, is_mine)
        self.assertTrue(self.img_choice.uncovered)


    def test_shows_face_depending_on_cover_status(self):
        self.assertEqual(self.img_choice.showable_face(), self.blurred)

        self.img_choice.uncover()

        self.assertEqual(self.img_choice.showable_face(), self.base)
