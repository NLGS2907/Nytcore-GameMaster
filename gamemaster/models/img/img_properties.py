from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, TypedDict

from PIL.Image import open as img_open

if TYPE_CHECKING:
    from io import BytesIO


class _ImagePropDict(TypedDict):
    "Dict version of the image properties."

    format: str
    width: int
    height: int
    size: int


@dataclass
class ImageProperties:
    """Helper type to hold a profile image's properties.
    
    Attributes:
        format: The image format of the image, like 'PNG' or 'JPEG'.
        width: The width in pixels of the image.
        height: The height in pixels of the image.
        size: The size in bytes of the image.
    """

    format: str
    width: int
    height: int
    size: int


    @classmethod
    def from_file(cls, file: "BytesIO") -> Self:
        """Creates a properties object from binary data.
        
        Args:
            file: A file-like object that contains the binary data.

        Returns:
            The properties object of said file.
        """

        with img_open(file) as img:
            format = img.format
            width, height = img.size
        size = file.getbuffer().nbytes
        file.seek(0)

        return cls(format, width, height, size)