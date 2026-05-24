from io import BytesIO
from typing import TYPE_CHECKING, Optional, TypeAlias, Union

from discord import Colour, File, SeparatorSpacing
from discord.ui import ActionRow, Container, Section, Separator, TextDisplay, Thumbnail

from ...models import IMG_FORMAT
from ..base_view import BaseView
from .edit_profile_btn import EditProfileButton
from .mention_user_btn import MentionUserButton
from .show_user_img_btn import ShowUserImageButton

if TYPE_CHECKING:
    from ...gamemaster import GameMaster
    from ...models import Player
    from ..base_view import PossibleMessage, PossibleUser

EitherButtonOrText: TypeAlias = Union[MentionUserButton, TextDisplay]

KB_IN_BYTES: int = 1024
MB_IN_BYTES: int = KB_IN_BYTES ** 2
GB_IN_BYTES: int = KB_IN_BYTES ** 3


class ProfileView(BaseView):
    """UI for interacting with profiles."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 player: "Player",
                 player_user: "PossibleUser",
                 *,
                 is_public: bool,
                 timeout: Optional[float]=None):
        """Initializes the profile view.
        
        Besides those of the parent class, there's a few extra arguments to consider.

        Args:
            bot: A reference to the bot user.
            parent_msg: A reference to the parent message that spawned this view.
            origin_user: The orignal user who sent the interaction. The parent message not
                         necessarily holds this information, as the bot is the author most of
                         the time.
            player: The player object to extract the data from.
            player_user: A helper object that is the Discord user object tied to the player.
                         Not necessarily the same as `origin_user`.
            is_public: Wether the profile is intended to be seen by others.
            timeout: Timeout, in seconds, from last interaction until the view becomes unresponsive.
        """
        super().__init__(bot, parent_msg, origin_user, timeout=timeout)

        self.player: "Player" = player
        self.player_user: "PossibleUser" = player_user
        self.all_files: list[File] = []
        self.__is_public: bool = is_public

        self.discord_user_section: Optional[Section] = None
        self.mention_user_component: Optional[EitherButtonOrText] = None


    @staticmethod
    def format_filesize(size_in_bytes: int) -> str:
        """Takes a number represeenting a size in bytes, and formats it to the closest modifier."""

        size_in_gb = size_in_bytes / GB_IN_BYTES
        if size_in_gb > 1:
            return f"{size_in_gb:.2f} GB"

        size_in_mb = size_in_bytes / MB_IN_BYTES
        if size_in_mb > 1:
            return f"{size_in_mb:.2f} MB"

        size_in_kb = size_in_bytes / KB_IN_BYTES
        if size_in_kb > 1:
            return f"{size_in_kb:.2f} KB"

        return f"{size_in_bytes} bytes"


    def _small_separator(self, container: Container):
        """Adds a small separator item to the container."""

        container.add_item(Separator(spacing=SeparatorSpacing.small))


    def _large_separator(self, container: Container):
        """Adds a large separator item to the container."""

        container.add_item(Separator(spacing=SeparatorSpacing.large))


    def _thumbnail_section(self, container: Container, fallback_img: "BytesIO") -> Section:
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


    def _discord_user_section(self,
                              container: Container,
                              profile_img_file: File) -> tuple[Section, EitherButtonOrText]:
        """Prepares the section for showing the Discord user info.
        
        Args:
            container: The container to which add the components.
            profile_img_file: The discord user profile image file.

        Returns:
            A tuple with the section and text label (or button) that were just added.
        """

        self.discord_user_section = Section("## Discord User",
                                            f"### Username: **{self.player_user.display_name}**",
                                            f"### User ID: `{self.player_user.id}`",
                                            accessory=ShowUserImageButton(self,
                                                                          Thumbnail(profile_img_file)))
        container.add_item(self.discord_user_section)

        if self.mention_user_component is None:
            self.mention_user_component = ActionRow(
                MentionUserButton(self,f"### Details: {self.player_user.mention}"))
        container.add_item(self.mention_user_component)

        return self.discord_user_section, self.mention_user_component


    def _emoji_section(self, container: Container) -> tuple[TextDisplay, TextDisplay, TextDisplay]:
        """Adds the parts for showing the player's emoji info to the container.
        
        Args:
            container: The container to which add the components.

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


    def _image_details_section(self, container: Container) -> tuple[TextDisplay, TextDisplay,
                                                                    TextDisplay, TextDisplay]:
        """Adds the profile image details section to the container.
        
        Args:
            container: The container to which add the components.

        Returns:
            A tuple with all the text labels that were just added.
        """

        img_props = self.player.image_properties

        img_title_text = TextDisplay("## Profile Image Details")
        container.add_item(img_title_text)

        img_fmt = (f"`{img_props['format'].upper()}`" if img_props is not None else "_None_")
        img_fmt_text = TextDisplay(f"### Format:\t{img_fmt}")
        container.add_item(img_fmt_text)

        img_dim = (f"{img_props['width']}x{img_props['height']} pixels"
                   if img_props is not None else "_N/A_")
        img_dim_text = TextDisplay(f"### Dimensions:\t{img_dim}")
        container.add_item(img_dim_text)

        img_size = (self.format_filesize(img_props['size']) if img_props is not None else "_N/A_")
        img_size_text = TextDisplay(f"### Size:\t{img_size}")
        container.add_item(img_size_text)

        return img_title_text, img_fmt_text, img_dim_text, img_size_text


    async def prepare(self):
        """Poblates the view with all the info about the player."""

        author_img = await self.bot.fetch_avatar(self.player_user)
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
        self._image_details_section(master_container)

        if not self.__is_public and (self.user == self.player_user):
            master_container.add_item(ActionRow(EditProfileButton(self.player,
                                                                  self.bot.repositories.player)))

        self.add_item(master_container)
        
