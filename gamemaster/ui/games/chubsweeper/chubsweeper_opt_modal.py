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


class ChubSweeperOptionsModal(BaseOptionsModal[ChubSweeperOptions]):
    """Options modal for a game of ChubSweeper."""

    def prepare(self):
        use_private_mode = Label(
            text="Activate Private Mode",
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
        

    def update_options(self):
        use_private_mode: Checkbox
        transform_width: TextInput
        transform_height: TextInput
        use_private_mode, transform_width, transform_height = self._unpack_components()

        validated_width = self._validate_transform(transform_width.value,
                                                   self.options.fixed_width)
        validated_height = self._validate_transform(transform_height.value,
                                                    self.options.fixed_height)

        self.options.private_mode = use_private_mode.value
        self.options.fixed_width = validated_width
        self.options.fixed_height = validated_height


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
