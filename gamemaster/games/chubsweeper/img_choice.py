from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .img_holder import ImagePairHolder, ImageType

class ImageChoice:
    """Object to track a singular image choice over the ocurse of a game."""

    def __init__(self, holder: "ImagePairHolder", is_mine: bool, number: int):
        """Initializes the choice.

        Args:
            holder: The image holder where to retrieve the images.
            is_mine: Wether the holder in question is a ChubMine.
            number: The number by which to identify this image.
        """

        self._holder: "ImagePairHolder" = holder
        self._mine: bool = is_mine
        self._uncovered: bool = False
        self._num: int = number
        self._num_blur: "ImageType" = self._holder.blurred_copy_with_number(number)


    @property
    def mine(self) -> bool:
        """Checks if the choice is a ChubMine."""

        return self._mine


    @property
    def uncovered(self) -> bool:
        """Checks if the choice was already made before."""

        return self._uncovered


    @property
    def number(self) -> int:
        """Retrieves the identifying number of this choice."""

        return self._num


    @property
    def numbered_blurred(self) -> "ImageType":
        """Retrieves the numbered blurred copy of the underlying image."""

        return self._num_blur


    def uncover(self) -> bool:
        """Uncovers the choice made.
        
        Returns:
            A boolean value indicating wether the choice uncovered was a ChubMine or not.
        """

        self._uncovered = True
        return self.mine


    def showable_face(self) -> "ImageType":
        """Retrieves the numbered blurred if not uncovered yet, or the normal image if so."""

        return (self._holder.base if self.uncovered else self.numbered_blurred)
