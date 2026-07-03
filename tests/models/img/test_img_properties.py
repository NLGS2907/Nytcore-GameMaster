from unittest import TestCase

from gamemaster.models import ImageProperties

from ...helper import dummy_bmp


class TestImageProperties(TestCase):
    def setUp(self):
        self.format = "PNG"
        self.width = 123
        self.height = 456
        self.size = 999999


    def test_is_initialized_correctly(self):
        img_props = ImageProperties(self.format, self.width, self.height, self.size)

        self.assertHasAttr(img_props, "format")
        self.assertEqual(img_props.format, self.format)

        self.assertHasAttr(img_props, "width")
        self.assertEqual(img_props.width, self.width)

        self.assertHasAttr(img_props, "height")
        self.assertEqual(img_props.height, self.height)

        self.assertHasAttr(img_props, "size")
        self.assertEqual(img_props.size, self.size)



    def test_can_initialize_from_file(self):
        img_file = dummy_bmp(self.width, self.height)
        img_format = "BMP"

        img_props = ImageProperties.from_file(img_file)

        self.assertEqual(img_props.format, img_format)
        self.assertEqual(img_props.width, self.width)
        self.assertEqual(img_props.height, self.height)
