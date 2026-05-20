from typing import TYPE_CHECKING, Optional, TypeAlias

if TYPE_CHECKING:
    from io import BytesIO

UsernameType: TypeAlias = str
DiscordUserIdType: TypeAlias = int
EmojiType: TypeAlias = str
ProfileImageType: TypeAlias = "BytesIO"

NAME_MIN_LENGTH: int = 3
NAME_MAX_LENGTH: int = 30


class Player:
    """Player model that holds all the data of a player profile.
    
    Attributes:
        username: The name of the player.
        discord_user_id: The discord user ID tied to the player.
        emoji: An optional emoji to be used in some minigames.
        profile_img: The custom profile image that the player chose.
    """

    def __init__(self,
                 username: UsernameType,
                 discord_user_id: DiscordUserIdType,
                 emoji: Optional[EmojiType]=None,
                 profile_img: Optional[ProfileImageType]=None):
        """Initializes the player user.
        
        Args:
            username: The name of the player.
            discord_user_id: The discord user ID tied to the player.
            emoji: An optional emoji to be used in some minigames.
            profile_img: The custom profile image that the player chose.
        """

        self._username: UsernameType = username
        self._discord_user_id: DiscordUserIdType = discord_user_id
        self._emoji: Optional[EmojiType] = emoji
        self._profile_img: Optional[ProfileImageType] = profile_img


    @property
    def username(self) ->  UsernameType:
        return self._username


    @username.setter
    def username(self, new_name: UsernameType):
        self._username = self.validate_name(new_name)


    @property
    def discord_user_id(self) ->  DiscordUserIdType:
        return self._discord_user_id


    @property
    def emoji(self) ->  Optional[EmojiType]:
        return self._emoji


    @property
    def profile_img(self) ->  Optional[ProfileImageType]:
        return self._profile_img


    @staticmethod
    def validate_name(candidate_name: UsernameType) -> UsernameType:
        """Validates if the given name is valid.
        
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
