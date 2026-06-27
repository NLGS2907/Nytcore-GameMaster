from unittest import TestCase

from gamemaster.models import ImageProperties


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



    def test_can_initialize_from_dict(self):
        props_dict = dict(format=self.format,
                          width=self.width,
                          height=self.height,
                          size=self.size)

        img_props = ImageProperties.from_dict(props_dict)

        self.assertEqual(img_props.format, props_dict["format"])
        self.assertEqual(img_props.width, props_dict["width"])
        self.assertEqual(img_props.height, props_dict["height"])
        self.assertEqual(img_props.size, props_dict["size"])
