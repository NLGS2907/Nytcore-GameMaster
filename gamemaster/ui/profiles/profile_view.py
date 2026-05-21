from io import BytesIO
from typing import TYPE_CHECKING, Optional, Union

from discord import Colour, File, SeparatorSpacing
from discord.ui import ActionRow, Container, Section, Separator, TextDisplay, Thumbnail

from ...models import IMG_FORMAT
from ..base_view import BaseView
from .mention_user_btn import MentionUserButton
from .show_user_img_btn import ShowUserImageButton

if TYPE_CHECKING:

    from discord import InteractionMessage

    from ...gamemaster import GameMaster
    from ...models import Player
    from ..base_view import PossibleUser


class ProfileView(BaseView):
    """UI for interacting with profiles."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "InteractionMessage",
                 player: "Player",
                 origin_user: "PossibleUser",
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, timeout=timeout)

        self.player: "Player" = player
        self.all_files: list[File] = []

        self.discord_user_section: Optional[Section] = None
        self.mention_user_component: Optional[Union[MentionUserButton, TextDisplay]] = None


    def _small_separator(self, container: Container):
        """Adds a small separator item to the container."""

        container.add_item(Separator(spacing=SeparatorSpacing.small))


    def _large_separator(self, container: Container):
        """Adds a large separator item to the container."""

        container.add_item(Separator(spacing=SeparatorSpacing.large))


    def _thumbnail_section(self, container: Container, fallback_img: "BytesIO"):
        """Prepares the section that contains the title and profile image.
        
        Args:
            container: The container to which add this section.
            fallback_img: In case the player doesn't have an image, use this one as thumbnail.

        Returns:
            The section that was just added, in case it is needed to store a reference.
        """

        player_img = self.player.profile_img
        thumbnail_file = File(player_img if player_img is not None else fallback_img,
                              filename=f"thumbnail.{IMG_FORMAT}")
        self.all_files.append(thumbnail_file)

        section = Section(f"# \"{self.player.username}\" Profile",
                          accessory=Thumbnail(thumbnail_file))
        container.add_item(section)

        return section


    def _discord_user_section(self, container: Container, profile_img_file: File) -> Section:
        """Prepares the section for showing the Discord user info.
        
        Args:
            container: The container to which add this section.
            profile_img_file: The discord user profile image file.

        Returns:
            A tuple with the section and text label that were just added.
        """

        self.discord_user_section = Section("## Discord User",
                                            f"### Username: **{self.user.display_name}**",
                                            f"### User ID: `{self.user.id}`",
                                            accessory=ShowUserImageButton(self,
                                                                          Thumbnail(profile_img_file)))
        container.add_item(self.discord_user_section)

        if self.mention_user_component is None:
            self.mention_user_component = ActionRow(
                MentionUserButton(self,f"### Details: {self.user.mention}"))
        container.add_item(self.mention_user_component)

        return self.discord_user_section, self.mention_user_component


    def _emoji_section(self, container: Container):
        """Adds the parts for showing the player's emoji info to the container.
        
        Args:
            container: The container to which add this section.

        Returns:
            A tuple with all the text labels that were just added.
        """

        emoji = self.player.emoji
        chosen_emoji = emoji if emoji else "_N/A_"
        raw_emoji = (f"`{self.bot.repositories.player.emoji_to_unicode(emoji)}`"
                     if emoji else "_N/A_")

        title_text = TextDisplay("## Emoji")
        container.add_item(title_text)

        emoji_text = TextDisplay(f"### Chosen Emoji:\t{chosen_emoji}")
        container.add_item(emoji_text)

        raw_emoji_text = TextDisplay(f"### Raw Emoji:\t{raw_emoji}")
        container.add_item(raw_emoji_text)

        return (title_text, emoji_text, raw_emoji_text)


    async def prepare(self):
        """Poblates the view with all the info about the player."""

        author_img = await self.bot.fetch_avatar(self.user)
        # we can't use the same image, it has to be a copy
        author_file = File(BytesIO(author_img.getvalue()), f"user.{IMG_FORMAT}")
        self.all_files.append(author_file)

        master_container = Container(accent_colour=Colour.random())

        self._thumbnail_section(master_container, author_img)
        self._large_separator(master_container)
        self._discord_user_section(master_container, author_file)
        self._small_separator(master_container)
        self._emoji_section(master_container)
        self._small_separator(master_container)

        self.add_item(master_container)
