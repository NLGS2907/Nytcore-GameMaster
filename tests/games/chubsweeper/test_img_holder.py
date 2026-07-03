from unittest import TestCase

from gamemaster.games import BlurLevel, ImagePairHolder, ImageType

from ...helper import dummy_bmp


class TestImagePairHolder(TestCase):
    def setUp(self):
        self.expected_format = "WEBP"


    def test_is_initialized_with_both_images(self):
        img_holder = ImagePairHolder(dummy_bmp(500, 500))

        self.assertHasAttr(img_holder, "base")
        self.assertIsInstance(img_holder.base, ImageType)

        self.assertHasAttr(img_holder, "blurred")
        self.assertIsInstance(img_holder.blurred, ImageType)


    def test_uses_default_blur_value(self):
        default_blur_lvl = BlurLevel.VERY_STRONG
        img_holder = ImagePairHolder(dummy_bmp(500, 500))

        self.assertHasAttr(img_holder, "blur_level")
        self.assertEqual(img_holder.blur_level, default_blur_lvl)


    def test_can_retrieve_properties_of_base_image(self):
        width = 500
        height = 450
        img_holder = ImagePairHolder(dummy_bmp(width, height))

        img_props = img_holder.base_properties

        self.assertIsNotNone(img_props)
        self.assertEqual(img_props.width, width)
        self.assertEqual(img_props.height, height)
        self.assertEqual(img_props.format.upper(), self.expected_format)


    def test_can_retrieve_properties_of_blurred_image(self):
        width = 760
        height = 800
        img_holder = ImagePairHolder(dummy_bmp(width, height))

        img_props = img_holder.blurred_properties

        self.assertIsNotNone(img_props)
        self.assertEqual(img_props.width, width)
        self.assertEqual(img_props.height, height)
        self.assertEqual(img_props.format.upper(), self.expected_format)


    def test_can_force_fixed_width(self):
        fixed_width = 500
        img_holder = ImagePairHolder(dummy_bmp(fixed_width + 100, 700), fixed_width=fixed_width)

        self.assertEqual(img_holder.base_properties.width, fixed_width)
        self.assertEqual(img_holder.blurred_properties.width, fixed_width)


    def test_can_force_fixed_height(self):
        fixed_height = 650
        img_holder = ImagePairHolder(dummy_bmp(580, fixed_height + 210), fixed_height=fixed_height)

        self.assertEqual(img_holder.base_properties.height, fixed_height)
        self.assertEqual(img_holder.blurred_properties.height, fixed_height)


    def test_can_reblur_the_image(self):
        original_blur_lvl = BlurLevel.MILD
        new_blur_lvl = BlurLevel.STRONG
        img_holder = ImagePairHolder(dummy_bmp(250, 350), blur_level=original_blur_lvl)

        self.assertEqual(img_holder.blur_level, original_blur_lvl)
        img_holder.reblur(new_blur_lvl)

        self.assertEqual(img_holder.blur_level, new_blur_lvl)