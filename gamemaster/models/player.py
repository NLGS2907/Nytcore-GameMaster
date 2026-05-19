from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from discord import User
    from io import BytesIO


class Player:
    """Player model that holds all the data of a player profile.
    
    Attributes:
        username: The name of the player.
        discord_user_id: The discord user ID tied to the player.
        emoji: An optional emoji to be used in some minigames.
        profile_img: The custom profile image that the player chose.
    """

    def __init__(self,
                 username: str,
                 discord_user_id: "User",
                 emoji: Optional[str]=None,
                 profile_img: Optional["BytesIO"]=None):
        """Initializes the player user.
        
        Args:
            username: The name of the player.
            discord_user_id: The discord user ID tied to the player.
            emoji: An optional emoji to be used in some minigames.
            profile_img: The custom profile image that the player chose.
        """

        self.username: str = username
        self.discord_user_id: "User" = discord_user_id
        self.emoji: Optional[str] = emoji
        self.profile_img: Optional["BytesIO"] = profile_img
