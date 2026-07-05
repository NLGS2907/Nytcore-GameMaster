from typing import Optional, Self

from ..options_base import BaseOptions
from .blur_level import BlurLevel

PRIVATE_MODE_DEFAULT: bool = False
FIXED_WIDTH_DEFAULT: Optional[int] = None
FIXED_HEIGHT_DEFAULT: Optional[int] = None
BLUR_LEVEL_DEFAULT: BlurLevel = BlurLevel.STRONG
AMOUNT_SAFES_DEFAULT: int = 3
AMOUNT_MINES_DEFAULT: int = 1


class ChubSweeperOptions(BaseOptions):
    """Options for a game of ChubSweeper.

    Attributes:
        private_mode: Wether to serve the round to the players in their respective
                      private channels.
        fixed_width: The fixed width (in pixels) to transform the images into, if given.
        fixed_height: The fixed height (in pixels) to transform the images into, if given.
        blur_level: The blur intensity used to obfuscate yet unexplored images.
    """

    def __init__(self, *,
                 private_mode: bool,
                 fixed_width: Optional[int],
                 fixed_height: Optional[int],
                 blur_level: BlurLevel,
                 amount_safes: int,
                 amount_mines: int):
        """Initializes the options for a game of ChubSweeper.
        
        Args:
            private_mode: Wether to serve the round to the players in their respective
                          private channels.
            fixed_width: The fixed width (in pixels) to transform the images into, if given.
            fixed_height: The fixed height (in pixels) to transform the images into, if given.
            blur_level: The blur intensity used to obfuscate yet unexplored images.
            amount_safes: The amount of safe images that are allowed in this game.
            amount_mines: The amount of ChubMines that are allowed in this game.
        """

        self.private_mode: bool = private_mode
        self.fixed_width: Optional[int] = fixed_width
        self.fixed_height: Optional[int] = fixed_height
        self.blur_level: BlurLevel = blur_level
        self.amount_safes: int = amount_safes
        self.amount_mines: int = amount_mines


    @classmethod
    def default(cls) -> Self:
        return cls(
            private_mode=PRIVATE_MODE_DEFAULT,
            fixed_width=FIXED_WIDTH_DEFAULT,
            fixed_height=FIXED_HEIGHT_DEFAULT,
            blur_level=BLUR_LEVEL_DEFAULT,
            amount_safes=AMOUNT_SAFES_DEFAULT,
            amount_mines=AMOUNT_MINES_DEFAULT
        )