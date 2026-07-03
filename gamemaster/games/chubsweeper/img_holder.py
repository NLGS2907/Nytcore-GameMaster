from io import BytesIO
from typing import TYPE_CHECKING, Optional, TypeAlias

from PIL.Image import open as img_open
from PIL.ImageFilter import GaussianBlur

from ...models import ImageProperties
from .blur_level import BlurLevel

if TYPE_CHECKING:
    from PIL.ImageFile import ImageFile

ImageType: TypeAlias = BytesIO

PREFERRED_IMG_FORMAT: str = "webp"


class ImagePairHolder:
    """Object that can hold the base image and its obfuscated counterpart.
    
    Attributes:
        base: The original image. This one is not obfuscated but may have been transformed
              into a given size.
        base_properties: Some extra properties of the base image.
        blurred: The blurred version of the image. It is always of the same width and height
                 as the base one.
        blurred_properties: The properties of the blurred image.
        blur_level: The blur level used to transform the base image into the blurred one.
    """

    def __init__(self, base_img: ImageType,
                 *,
                 blur_level: BlurLevel=BlurLevel.VERY_STRONG,
                 fixed_width: Optional[int]=None,
                 fixed_height: Optional[int]=None):
        """Initializes the image holder.
        
        Args:
            base_img: The image to obfuscate.
            blur_level: The intensity of the blur.
            fixed_width: If given, force the images to this width.
            fixed_height: If given, force the images to this height.
        """

        self._base_img: ImageType = self._transform_dim(base_img, fixed_width, fixed_height)
        self._base_props: Optional[ImageProperties] = None

        self._preferred_blur_lvl: BlurLevel = blur_level
        self._blurred_img: ImageType = self._blur_image(self._base_img)
        self._blurred_props: Optional[ImageProperties] = None


    @property
    def base(self) -> ImageType:
        """Retrieves the base image of the pair."""

        return self._base_img


    @property
    def base_properties(self) -> ImageProperties:
        """Queries the base image and lazy loads its properties."""

        return self._load_properties(self._base_props, self._base_img)


    @property
    def blurred(self) -> ImageType:
        """Retrieves the blurred image of the pair."""

        return self._blurred_img


    @property
    def blurred_properties(self) -> ImageProperties:
        """Queries the blurred image and lazy loads its properties."""

        return self._load_properties(self._blurred_props, self._blurred_img)


    @property
    def blur_level(self) -> BlurLevel:
        """Retrieves the blur level used by this holder."""

        return self._preferred_blur_lvl


    @staticmethod
    def _load_properties(properties: Optional[ImageProperties], img: ImageType) -> ImageProperties:
        """Lazy loads the properties of an image and stores it.
        
        Args:
            properties: Where to store the loaded properties.
            img: The base image to query.

        Returns:
            The properties object.
        """

        if properties is None:
            properties = ImageProperties.from_file(img)

        return properties


    def _save_img(self, image_file: "ImageFile", target_file: ImageType):
        """Saves the images with the preferred format.
        
        Args:
            image_file: The image handler.
            target_file: The binary buffer to save the image to.
        """

        image_file.convert("RGBA").save(target_file, format=PREFERRED_IMG_FORMAT, lossless=True)
        target_file.seek(0)


    def _transform_dim(self,
                       img: ImageType,
                       fixed_width: Optional[int],
                       fixed_height: Optional[int]) -> ImageType:
        """Transforms the image to the given size if needed.

        Args:
            img: The image to transform.
            fixed_width: The width to force the image into, if given.
            fixed_height: The height to force the image into, if given.

        Returns:
            The transformed image with its new dimensions, or a copy of the original if none
            of them were specified. Do note however that it will be converted to a preferred
            format for optimized storing.
        """

        copied_img = ImageType()
        image = None
        try:
            image = img_open(img)

            if fixed_width is not None:
                image = image.resize((fixed_width, image.height))

            if fixed_height is not None:
                image = image.resize((image.width, fixed_height))

            self._save_img(image, copied_img)
        finally:
            if image is not None:
                image.close()

        img.seek(0) # just in case
        return copied_img


    def _blur_image(self, img: ImageType) -> ImageType:
        """Blurs the given image with the preferred blur level."""

        blurred_img = ImageType()
        with img_open(img) as image:
            blurred_image = image.filter(GaussianBlur(radius=self._preferred_blur_lvl.value))
            self._save_img(blurred_image, blurred_img)

        return blurred_img


    def reblur(self, blur_lvl: BlurLevel):
        """Modifies the blurred image inplace with the new blur level."""

        self._preferred_blur_lvl = blur_lvl
        self._blurred_img = self._blur_image(self._base_img)
