from random import shuffle
from typing import TYPE_CHECKING, TypeAlias

from .img_choice import ImageChoice

if TYPE_CHECKING:
    from .chubsweeper_game import HoldersList
    from .img_holder import ImageType

ImgChoicesList: TypeAlias = list[ImageChoice]


class ChoiceTracker:
    """Object that can track the choices of a player of ChubSweeper."""

    def __init__(self, *, safes: "HoldersList", mines: "HoldersList"):
        """Initializes the tracker.
        
        Args:
            safes: The holders of the safe images.
            mines: The holders of the ChubMines.
        """

        self._choices: ImgChoicesList = self._generate_choices(safes, mines)
        self._score: int = 0
        self._doomed: bool = False


    def _generate_choices(self, safes: "HoldersList", mines: "HoldersList") -> ImgChoicesList:
        """Generates all the image choices.
        
        Args:
            safes: The holders of the safe images.
            mines: The holders of the ChubMines.

        Returns:
            A list with all the image choices already numbered and initialized.
        """

        choices = [*((safe, False) for safe in safes), *((mine, True) for mine in mines)]
        shuffle(choices)

        return [
            ImageChoice(holder, is_mine, i)
            for i, (holder, is_mine) in enumerate(choices, start=1)
        ]


    @property
    def score(self) -> int:
        """Returns how many safes images the player has correctly guessed."""

        return self._score


    @property
    def doomed(self) -> bool:
        """Checks if the players has chosen at least one ChubMine."""

        return self._doomed


    def _get_choice(self, n: int) -> ImageChoice:
        """Retrieves the image choice of the given number."""

        return self._choices[n - 1]


    def numbered_blurred(self) -> list["ImageType"]:
        """Retrieves all numbered blurred copies of the underlying images."""

        return [choice.numbered_blurred for choice in self._choices]


    def is_mine(self, n: int) -> bool:
        """Determines if the given choice is a mine."""

        return self._get_choice(n).mine


    def uncovered(self, n: int) -> bool:
        """Checks if a choice of the given number was already made."""

        return self._get_choice(n).uncovered


    def uncover(self, n: int) -> bool:
        """Uncovers the choice of the given number.

        Args:
            n: The number of the image to retrieve.

        Returns:
            A boolean value indicating if the players has lost due to this choice.
        """

        if self._get_choice(n).uncover():
            self._doomed = True
        else:
            self._score += 1

        return self.doomed
