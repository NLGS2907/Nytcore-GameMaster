"""Module for profile editing modal."""

from io import BytesIO
from typing import TYPE_CHECKING

from discord import TextStyle
from discord.ui import FileUpload, Label, TextInput

from ...models import IMG_MAX_SIZE, IMG_MIN_SIZE, MAX_COLOR_DIGITS, NAME_MAX_LENGTH
from ..base_modal import BaseModal

if TYPE_CHECKING:
    from discord import Attachment, Interaction

    from ...models import Player
    from ...repositories import IPlayerRepository


class ProfileEditModal(BaseModal):
    """Asks for info to edit the profile of a user.

    Attributes:
        player: A player to hold the profile details with.
        player_repo: A player repository to actually save the changed properties.
    """

    def __init__(self, player: "Player", player_repository: "IPlayerRepository"):
        """Initializes the profile editing modal.
        
        Args:
            player: The player whose details to edit.
            player_repository: The repository from which to load and save players.
        """

        self.player: "Player" = player
        self.player_repo: "IPlayerRepository" = player_repository

        super().__init__(title=f" Edit {player.username} Profile Details", timeout=None)


    @property
    def error_message(self):
        return "It seems there was an error updating your profile."


    @property
    def success_message(self):
        player_name: TextInput
        emoji_selection: TextInput
        selected_color: TextInput
        profile_upload: FileUpload
        player_name, emoji_selection, selected_color, profile_upload = self._unpack_components()

        no_changes = not (player_name.value
                          or emoji_selection.value
                          or selected_color.value
                          or profile_upload.values)
        return ("No changes were made." if no_changes else "Your profile was updated successfully!")


    def prepare(self):
        image_description = (f"Square image of {IMG_MIN_SIZE}x{IMG_MIN_SIZE} "
                             f"- {IMG_MAX_SIZE}x{IMG_MAX_SIZE} in size. "
                             "If not square, it will be transformed so that it is.")

        self.add_item(Label(text="Player name",
                            description=f"Up to {NAME_MAX_LENGTH} characters.",
                            component=TextInput(style=TextStyle.short,
                                                required=False,
                                                min_length=0,
                                                placeholder=self.player.username)))
        self.add_item(Label(text="Emoji",
                            description="Only unicode, single character emojis are allowed.",
                            component=TextInput(style=TextStyle.short,
                                                required=False,
                                                min_length=0,
                                                placeholder=self.player.emoji)))
        self.add_item(Label(text="Favourite Color",
                            description="A color of your preference, in #rrggbb format.",
                            component=TextInput(style=TextStyle.short,
                                                required=False,
                                                min_length=0,
                                                max_length=MAX_COLOR_DIGITS + 1,
                                                placeholder=self.player.fav_color)))
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

        if not self._is_image(attachment):
            raise TypeError("Attached file does not seem to be an image")

        img_file = BytesIO()
        await attachment.save(img_file, seek_begin=True)
        self.player.profile_img = img_file


    async def callback(self, interaction: "Interaction"):
        player_name: TextInput
        emoji_selection: TextInput
        selected_color: TextInput
        profile_upload: FileUpload
        player_name, emoji_selection, selected_color, profile_upload = self._unpack_components()

        if player_name.value:
            self.player.username = player_name.value.strip()

        if emoji_selection.value:
            self.player.emoji = emoji_selection.value.strip()

        if profile_upload.values:
            await self._change_profile_image(profile_upload.values[0])

        if selected_color.value:
            self.player.fav_color = selected_color.value.strip()

        self.player_repo.save(self.player)
