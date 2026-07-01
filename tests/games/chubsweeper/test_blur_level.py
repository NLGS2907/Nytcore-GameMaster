from unittest import TestCase

from gamemaster.games import BlurLevel


class TestBlurLevel(TestCase):
    def test_is_initialized_properly(self):
        self.assertHasAttr(BlurLevel, "MILD")
        self.assertEqual(BlurLevel.MILD, 30)

        self.assertHasAttr(BlurLevel, "MEDIUM")
        self.assertEqual(BlurLevel.MEDIUM, 50)

        self.assertHasAttr(BlurLevel, "STRONG")
        self.assertEqual(BlurLevel.STRONG, 100)

        self.assertHasAttr(BlurLevel, "VERY_STRONG")
        self.assertEqual(BlurLevel.VERY_STRONG, 250)

        self.assertHasAttr(BlurLevel, "NONE")
        self.assertEqual(BlurLevel.NONE, 0)

        self.assertHasAttr(BlurLevel, "OPAQUE")
        self.assertEqual(BlurLevel.OPAQUE, -1)
