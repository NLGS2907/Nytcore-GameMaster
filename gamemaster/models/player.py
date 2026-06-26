from io import BytesIO
from re import compile
from typing import TYPE_CHECKING, Optional, TypeAlias, TypedDict

from emoji import is_emoji
from PIL.Image import open as img_open

if TYPE_CHECKING:
    from re import Pattern

UsernameType: TypeAlias = str
DiscordUserIdType: TypeAlias = int
EmojiType: TypeAlias = str
ProfileImgType: TypeAlias = BytesIO
ColorType: TypeAlias = str

NAME_MIN_LENGTH: int = 3
NAME_MAX_LENGTH: int = 30

IMG_MIN_SIZE: int = 250
IMG_MAX_SIZE: int = 1500
IMG_FORMAT: str = "webp"

MAX_COLOR_DIGITS: int = 6
COLOR_PATTERN: "Pattern" = compile(r"^#([0-9a-fA-F]){6}$")


class _ImageProperties(TypedDict):
    """Helper type to hold a profile image's properties."""

    format: str
    width: int
    height: int
    size: int


class Player:
    """Player model that holds all the data of a player profile.
    
    Attributes:
        username: The name of the player.
        discord_user_id: The discord user ID tied to the player.
        emoji: An optional emoji to be used in some minigames.
        profile_img: The custom profile image that the player chose.
        fav_color: The favourite color of the player, in #rrggbb format.
    """

    def __init__(self,
                 id: int,
                 username: UsernameType,
                 discord_user_id: DiscordUserIdType,
                 emoji: Optional[EmojiType]=None,
                 profile_img: Optional[ProfileImgType]=None,
                 fav_color: Optional[ColorType]=None):
        """Initializes the player user.
        
        Args:
            id: The underlying dataset ID.
            username: The name of the player.
            discord_user_id: The discord user ID tied to the player.
            emoji: An optional emoji to be used in some minigames.
            profile_img: The custom profile image that the player chose.
            fav_color: The favourite color of the player, in #rrggbb format.
        """

        self._id: int = id
        self._username: UsernameType = self._validate_name(username)
        self._discord_user_id: DiscordUserIdType = discord_user_id
        self._emoji: Optional[EmojiType] = self._validate_emoji(emoji)
        self._profile_img: Optional[ProfileImgType] = self._validate_profile_img(profile_img)
        self._fav_color: Optional[ColorType] = self._validate_fav_color(fav_color)

        self.__img_props: Optional[_ImageProperties] = None


    @property
    def id(self) -> int:
        return self._id


    @property
    def username(self) ->  UsernameType:
        return self._username


    @username.setter
    def username(self, new_name: UsernameType):
        self._username = self._validate_name(new_name)


    @property
    def discord_user_id(self) ->  DiscordUserIdType:
        return self._discord_user_id


    @property
    def emoji(self) ->  Optional[EmojiType]:
        return self._emoji


    @emoji.setter
    def emoji(self, new_emoji: Optional[EmojiType]):
        self._emoji = self._validate_emoji(new_emoji)


    @property
    def profile_img(self) ->  Optional[ProfileImgType]:
        return self._profile_img


    @profile_img.setter
    def profile_img(self, new_img: Optional[ProfileImgType]):
        self._profile_img = self._validate_profile_img(new_img)
        self.__img_props = None


    @property
    def fav_color(self) -> Optional[ColorType]:
        return self._fav_color


    @fav_color.setter
    def fav_color(self, new_color: Optional[ColorType]):
        self._fav_color = self._validate_fav_color(new_color)


    @property
    def image_properties(self) -> Optional[_ImageProperties]:
        """Returns a dictionary with some properties about the profile's image, if available.
        
        This is a helper property that lazy loads the image when it is first fetched,
        and then refers to it from memory.
        """

        if self.profile_img is None:
            return None

        if self.__img_props is None:
            self.__img_props = {}
            with img_open(self.profile_img) as img:
                self.__img_props["format"] = img.format
                width, height = img.size
                self.__img_props["width"] = width
                self.__img_props["height"] = height
            self.__img_props["size"] = self.profile_img.getbuffer().nbytes
            self.profile_img.seek(0)

        return self.__img_props


    @staticmethod
    def _validate_name(candidate_name: UsernameType) -> UsernameType:
        """Validates if the given name is correct.
        
        Args:
            candidate_name: The name to validate.

        Raises:
            TypeError: If the name isn't a string.
            ValueError: If the name is empty or isn't between the min and max length allowed.

        Returns:
            The same name, if validated successfully.
        """

        if not isinstance(candidate_name, UsernameType):
            raise TypeError(f"candidate name is of type {type(candidate_name).__name__!r}, "
                            f"but a name of type {UsernameType.__name__!r} is required.")

        sanitized_name = candidate_name.strip()
        if not sanitized_name:
            raise ValueError("given name appears to have only blank space.")

        name_len = len(sanitized_name)
        if name_len < NAME_MIN_LENGTH:
            raise ValueError(f"given name {sanitized_name!r} has length {name_len}, but one of "
                             f"at least {NAME_MIN_LENGTH} is required.")

        if name_len > NAME_MAX_LENGTH:
            raise ValueError(f"given name {sanitized_name!r} has length {name_len}, but only one "
                             f"up to {NAME_MAX_LENGTH} is allowed.")

        return sanitized_name


    @staticmethod
    def _validate_emoji(candidate_emoji: Optional[EmojiType]) -> Optional[EmojiType]:
        """Validates if the given emoji is correct.

        The input must be an emoji character, or `None` if it is omitted.

        Args:
            candidate_emoji: The emoji to validate.

        Raises:
            TypeError: If the emoji isn't a string.
            ValueError: If the input is empty, not an emoji char, or not a single char.

        Returns:
            A stripped version of the emoji, provided it was successfully validated.
        """

        if candidate_emoji is None:
            return None

        if not isinstance(candidate_emoji, EmojiType):
            raise TypeError(f"candidate emoji is of type {type(candidate_emoji).__name__!r}, "
                            f"but one of type {EmojiType.__name__!r} is required.")

        stripped_emoji = candidate_emoji.strip()
        if not stripped_emoji:
            raise ValueError("given emoji appears to be blank space")

        stripped_emoji_len = len(stripped_emoji)
        if stripped_emoji_len > 1:
            raise ValueError(f"The given input {stripped_emoji!r} must be comprised of only one "
                             f"char, yet it appears to be made of {stripped_emoji_len}")

        if not is_emoji(stripped_emoji):
            raise ValueError(f"The given input {stripped_emoji!r} does not seem to correspond "
                             "to an emoji character")

        return stripped_emoji


    @staticmethod
    def _validate_profile_img(candidate_img: Optional[ProfileImgType]) -> Optional[ProfileImgType]:
        """Validates if the given profile image is correct.

        Args:
            candidate_img: The profile image to validate.

        Raises:
            TypeError: If the image is not a file-like object.
            ValueError: If the image is too small or too big.

        Returns:
            An image compatible with the player object. If needed, it is transformed to size.
        """

        if candidate_img is None:
            return None

        if not isinstance(candidate_img, ProfileImgType):
            raise TypeError(f"candidate image is of type {type(candidate_img).__name__!r}, "
                            f"but one of type {ProfileImgType.__name__!r} is required.")

        result_img = ProfileImgType()
        img = None
        try:
            img = img_open(candidate_img)
            width = img.width
            height = img.height

            if width < IMG_MIN_SIZE or height < IMG_MIN_SIZE:
                raise ValueError("Image too small. Should be at least "
                                 f"{IMG_MIN_SIZE}x{IMG_MIN_SIZE} but is {width}x{height} instead")

            if width > IMG_MAX_SIZE or height > IMG_MAX_SIZE:
                raise ValueError(f"Image too big. Should be {IMG_MAX_SIZE}x{IMG_MAX_SIZE} "
                                 f"maximum, but is {width}x{height} instead")

            if width > height:
                img = img.resize((height, height))
            elif height > width:
                img = img.resize((width, width))

            img.convert("RGBA").save(result_img, format=IMG_FORMAT, lossless=True)
            result_img.seek(0)
        finally:
            if img is not None:
                img.close()

        return result_img


    @staticmethod
    def _validate_fav_color(candidate_color: Optional[ColorType]) -> Optional[ColorType]:
        """Validates if the given color is correct.

        Args:
            candidate_color: The color to validate.

        Raises:
            TypeError: If the color is not a string.
            ValueError: If the color doesn't follow a #rrggbb format, or is malformed
                        in another way.

        Returns:
            The color, already validated.
        """

        if candidate_color is None:
            return None

        if not isinstance(candidate_color, ColorType):
            raise TypeError(f"candidate color is of type {type(candidate_color).__name__!r}, "
                            f"but one of type {ProfileImgType.__name__!r} is required.")

        if COLOR_PATTERN.match(candidate_color) is None:
            raise ValueError((f"The color {candidate_color!r} has an invalid format. It should "
                              "follow the format #rrggbb."))

        return candidate_color.upper()
