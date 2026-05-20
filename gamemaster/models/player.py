from typing import TYPE_CHECKING, Optional, TypeAlias

if TYPE_CHECKING:
    from io import BytesIO

UsernameType: TypeAlias = str
DiscordUserIdType: TypeAlias = int
EmojiType: TypeAlias = str
ProfileImageType: TypeAlias = "BytesIO"


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


    @property
    def discord_user_id(self) ->  DiscordUserIdType:
        return self._discord_user_id


    @property
    def emoji(self) ->  Optional[EmojiType]:
        return self._emoji


    @property
    def profile_img(self) ->  Optional[ProfileImageType]:
        return self._profile_img

