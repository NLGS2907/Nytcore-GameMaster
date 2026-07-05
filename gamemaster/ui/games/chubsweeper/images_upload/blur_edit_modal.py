from typing import TYPE_CHECKING

from discord import RadioGroupOption
from discord.ui import Label, RadioGroup

from .....games import BlurLevel
from ....base_modal import BaseModal

if TYPE_CHECKING:
    from discord import Interaction

    from .img_upload_view import ChubMinesUploadView


class BlurEditModal(BaseModal):
    """Modal for editing the blur of the images of a game of ChubSweeper."""

    def __init__(self, parent_view: "ChubMinesUploadView"):
        """Initializes the mines upload modal.
        
        Args:
            parent_view: The mines upload view, to save the images.
        """

        self.parent_view: "ChubMinesUploadView" = parent_view

        super().__init__(title="ChubMines™ Images Blur", timeout=None)


    @property
    def error_message(self):
        return "Something happened while trying to blur the images."


    @property
    def success_message(self):
        return "Blur level of images edited successfully."


    def prepare(self):
        current_lvl = self.parent_view.game.options.blur_level
        blur_level_setting = RadioGroup(
            required=True,
            options=[
                RadioGroupOption(
                    label=lvl.name.replace("_", " ").capitalize(),
                    value=lvl.value,
                    default=(lvl == current_lvl)
                ) for lvl in BlurLevel if lvl != BlurLevel.NONE
            ]
        )
        blur_level = Label(
            text="Blur Level",
            description="The new level of obfuscation to use for the images on each round.",
            component=blur_level_setting
        )
        self.add_item(blur_level)


    async def callback(self, interaction: "Interaction"):
        blur_level: RadioGroup
        blur_level, = self._unpack_components()

        self.parent_view.reblur_images(BlurLevel(int(blur_level.value)))
        await self.parent_view.refresh(interaction)