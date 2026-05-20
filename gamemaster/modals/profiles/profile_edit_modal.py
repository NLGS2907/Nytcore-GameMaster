"""Module for profile editing modal."""

from io import BytesIO
from typing import TYPE_CHECKING

from discord import TextStyle
from discord.ui import FileUpload, Label, Modal, TextInput

from ...models import IMG_MAX_SIZE, IMG_MIN_SIZE
from ...repositories import PlayerRepository

if TYPE_CHECKING:
    from discord import Attachment, Interaction

    from ...models import Player


class ProfileEditModal(Modal):
    """Asks for info to edit the profile of a user."""

    def __init__(self, player: "Player"):
        """Initializes the profile editing modal.
        
        Args:
            player: The player whose details to edit.
        """

        super().__init__(title=f"{player.username} Profile Details", timeout=None)
        self.player: "Player" = player

        image_description = (f"Square image of {IMG_MIN_SIZE}x{IMG_MIN_SIZE} "
                             f"- {IMG_MAX_SIZE}x{IMG_MAX_SIZE} in size. "
                             "If not square, it will be transformed so that it is.")

        self.add_item(Label(text="Player name",
                            component=TextInput(style=TextStyle.short,
                                                required=False,
                                                min_length=0,
                                                placeholder=player.username)))
        self.add_item(Label(text="Emoji",
                            description="Only unicode, single character emojis are allowed.",
                            component=TextInput(style=TextStyle.short,
                                                required=False,
                                                min_length=0,
                                                placeholder=player.emoji)))
        self.add_item(Label(text="Profile image",
                            description=image_description,
                            component=FileUpload(required=False, min_values=0, max_values=1)))


    async def _change_profile_image(self, attachment: "Attachment"):
        """Tries to save the image to the player object.
        
        Args:
            attachment: The discord attachment with the file metadata.

        Raises:
            TypeError: If the media type of the file isn't that of an image.
        """

        if "image" not in attachment.content_type:
            raise TypeError("Attached file does not seem to be an image")

        img_file = BytesIO()
        await attachment.save(img_file, seek_begin=True)
        self.player.profile_img = img_file


    async def on_submit(self, interaction: "Interaction"):
        """The user sucessfully sent the profile editing modal."""

        player_name, emoji_selection, files_upload = map(lambda label: label.component,
                                                         self.children)
        
        try:
            player_repo = PlayerRepository()

            if player_name.value:
                self.player.username = player_name.value.strip()

            if emoji_selection.value:
                self.player.emoji = emoji_selection.value.strip()

            if files_upload.values:
                await self._change_profile_image(files_upload.values[0])

            player_repo.save(self.player)
        except (TypeError, ValueError) as err:
            msg = f"**[ERROR]** It seems there was an error updating your profile.\n\n> _{err}_"
            await interaction.response.send_message(msg, ephemeral=True)

            raise err from err

        await interaction.response.send_message("_Your profile was updated successfully!_",
                                                ephemeral=True)

        
