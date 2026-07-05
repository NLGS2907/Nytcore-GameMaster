from re import ASCII, compile
from typing import TYPE_CHECKING, Optional

from discord import TextStyle
from discord.ui import Checkbox, Label, TextInput

from ....games import ChubSweeperOptions
from ..options_modal_base import BaseOptionsModal

if TYPE_CHECKING:
    from re import Pattern

TRANSFORM_MIN: int = 50
TRANSFORM_MAX: int = 1500
TRANSFORM_PATTERN: "Pattern" = compile(r'^-?(0|[1-9]\d*)$', flags=ASCII)

AMOUNT_MIN: int = 1
AMOUNT_MAX: int = 10 # Discord limitation, not my fault


class ChubSweeperOptionsModal(BaseOptionsModal[ChubSweeperOptions]):
    """Options modal for a game of ChubSweeper."""

    def prepare(self):
        use_private_mode = Label(
            text="[WIP] Activate Private Mode",
            description="Each player will be served the images in their own DMs.",
            component=Checkbox(
                default=self.options.private_mode
            )
        )
        self.add_item(use_private_mode)

        transform_width = Label(
            text="Fixed Width",
            description=("Amount (in pixels) to stretch the width of the images to. "
                         "Input a negative numer to ignore."),
            component=TextInput(
                style=TextStyle.short,
                placeholder=(str(self.options.fixed_width)
                             if self.options.fixed_width is not None else None),
                required=False,

            )
        )
        self.add_item(transform_width)

        transform_height = Label(
            text="Fixed Height",
            description=("Amount (in pixels) to stretch the height of the images to. "
                         "Input a negative numer to ignore."),
            component=TextInput(
                style=TextStyle.short,
                placeholder=(str(self.options.fixed_height)
                             if self.options.fixed_height is not None else None),
                required=False,

            )
        )
        self.add_item(transform_height)

        range_msg = f"You can upload between {AMOUNT_MIN} and {AMOUNT_MAX} images."

        amount_safes = Label(
            text="Amount of Safe Images",
            description=f"How many \"safes\" to upload for each round. {range_msg}",
            component=TextInput(
                style=TextStyle.short,
                placeholder=self.options.amount_safes,
                required=False
            )
        )
        self.add_item(amount_safes)

        amount_safes = Label(
            text="Amount of ChubMines",
            description=f"How many mines to upload for each round. {range_msg}",
            component=TextInput(
                style=TextStyle.short,
                placeholder=self.options.amount_mines,
                required=False
            )
        )
        self.add_item(amount_safes)
        

    def update_options(self):
        use_private_mode: Checkbox
        transform_width: TextInput
        transform_height: TextInput
        amount_safes: TextInput
        amount_mines: TextInput
        (use_private_mode, transform_width, transform_height,
         amount_safes, amount_mines) = self._unpack_components()

        validated_width = self._validate_transform(transform_width.value,
                                                   self.options.fixed_width)
        validated_height = self._validate_transform(transform_height.value,
                                                    self.options.fixed_height)
        validated_safes = self._validate_amount(amount_safes.value, self.options.amount_safes)
        validated_mines = self._validate_amount(amount_mines.value, self.options.amount_mines)

        self.options.private_mode = use_private_mode.value
        self.options.fixed_width = validated_width
        self.options.fixed_height = validated_height
        self.options.amount_safes = validated_safes
        self.options.amount_mines = validated_mines


    def _validate_transform(self, px: str, default: Optional[int]) -> Optional[int]:
        """Checks if the given transform value is a valid number.
        
        Args:
            px: The value in pixels of the desired transform dimension.
            default: The default value to return, in case `px` is valid but empty.

        Raises:
            ValueError: If the transform value isn't numeric nature, or not in the allowed range.

        Returns:
            The transform dimension, already validated.
        """

        if not px:
            return default

        if not TRANSFORM_PATTERN.match(px):
            raise ValueError(f"Transform value {px!r} is not a valid number.")

        num_px = int(px)
        if num_px < 0:
            return None

        if num_px < TRANSFORM_MIN or num_px > TRANSFORM_MAX:
            raise ValueError(f"Transform value {px} should be in the range "
                             f"[{TRANSFORM_MIN}, {TRANSFORM_MAX}]")

        return num_px


    def _validate_amount(self, amount: str, default: int) -> int:
        """Checks if the given string is in the correct format for an amount of images.
        
        Args:
            amount: The string containing the amount to check.
            default: A default value to return in case of invalid amount.

        Raises:
            ValueError: If the given amount is numeric or not in the allowed range.

        Returns:
            The validated amount, ready to be stored.
        """

        if not amount:
            return default

        if not amount.isdecimal():
            raise ValueError(f"Amount of images {amount} does not seem to be a valid number.")

        num_amount = int(amount)
        if num_amount < AMOUNT_MIN or num_amount > AMOUNT_MAX:
            raise ValueError(f"Amount of images {amount} should be in the range "
                             f"[{AMOUNT_MIN}, {AMOUNT_MAX}].")

        return num_amount
