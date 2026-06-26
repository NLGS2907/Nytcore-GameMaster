from dataclasses import dataclass
from typing import Self, TypedDict


class _ImagePropDict(TypedDict):
    "Dict version of the image properties."

    format: str
    width: int
    height: int
    size: int


@dataclass
class ImageProperties:
    """Helper type to hold a profile image's properties."""

    format: str
    width: int
    height: int
    size: int


    @classmethod
    def from_dict(cls, props: _ImagePropDict) -> Self:
        "Instantiates an object from the dict version."

        return cls(props["format"], props["width"], props["height"], props["size"])