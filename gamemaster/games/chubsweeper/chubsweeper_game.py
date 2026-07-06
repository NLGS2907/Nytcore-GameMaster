from random import shuffle
from typing import TYPE_CHECKING, Iterable, Optional, TypeAlias

from ..game_base import BaseGame
from .chubsweeper_options import ChubSweeperOptions
from .img_holder import ImagePairHolder

if TYPE_CHECKING:
    from io import BytesIO

    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...models import Player
    from ..game_base import EmojisCollection
    from .blur_level import BlurLevel

HoldersList: TypeAlias = list[ImagePairHolder]
FilesIter: TypeAlias = Iterable["BytesIO"]
FilesList: TypeAlias = list["BytesIO"]


class ChubSweeperGame(BaseGame[ChubSweeperOptions]):
    """Game class for a game of ChubSweeper.

    Attributes:
        bot: A reference to the bot user.
        host_user: The original user that started the game.
        players: A list of all the players involved in the game.
        options: The options object of this game, if available.
    """

    def __init__(self,
                 bot: "GameMaster",
                 host_user: "User",
                 players: list["Player"],
                 *,
                 options: ChubSweeperOptions):
        super().__init__(bot, host_user, players, options=options)
        self._dealer, self._miners = self._distinguish_players()
        self._safes: HoldersList = []
        self._mines: HoldersList = []


    @staticmethod
    def title_name() -> str:
        return "ChubSweeper"


    @staticmethod
    def description() -> Optional[str]:
        return "Try to avoid landing on the ChubMines™, while appreciating the \"safes\"."


    @staticmethod
    def emojis_collection() -> "EmojisCollection":
        return ["🤰🏻", "🫃🏻", "🫄🏻"]


    @staticmethod
    def minimum_players() -> int:
        return 2


    @staticmethod
    def maximum_players() -> int:
        return 9


    def _distinguish_players(self) -> tuple["Player", list["Player"]]:
        """Tries to separate the host player from the rest.
        
        Raises:
            ValueError: If, somehow, the host user isn't in the player's list.

        Returns:
            A tuple where the first element is the host user (a.k.a. the \"Dealer\"), and the
            second element is a list of the rest of the players (i.e. the \"Miners\").
        """

        dealer = None
        miners = []
        for player in self.players:
            if player.discord_user_id == self.host_user.id:
                dealer = player
            else:
                miners.append(player)

        if dealer is None:
            raise ValueError("No dealer detected in this game. "
                             f"It should be the user with id {self.host_user.id!r}")

        return dealer, miners


    @property
    def dealer(self) -> "Player":
        """Fetches the host user of this game."""

        return self._dealer


    @property
    def miners(self) -> list["Player"]:
        """Fetches the players of this game, other than the host."""

        return self._miners


    @property
    def safes(self) -> HoldersList:
        """Fetches the safe images holders."""

        return self._safes


    @property
    def mines(self) -> HoldersList:
        """Fetches the safe images holders."""

        return self._mines


    def _generate_img_holders(self, files: FilesIter) -> HoldersList:
        """Generates a image holder for every element in the files iterable."""

        return [
            ImagePairHolder(
                file,
                blur_level=self.options.blur_level,
                fixed_width=self.options.fixed_width,
                fixed_height=self.options.fixed_height
            )
            for file in files
        ]


    def set_safes(self, safes: FilesIter):
        """Saves all the given images into the safe images list."""

        self._safes = self._generate_img_holders(safes)


    def set_mines(self, mines: FilesIter):
        """Saves all the given images into the ChubMines list."""

        self._mines = self._generate_img_holders(mines)


    def reblur_images(self, blur_level: "BlurLevel"):
        """Tries to obfuscate the images again, without resetting the holders.
        
        Args:
            blur_level: The new obfuscation intensity.
        """

        self.options.blur_level = blur_level

        for safe in self._safes:
            safe.reblur(blur_level)

        for mine in self._mines:
            mine.reblur(blur_level)


    def _load_blurred(self, images: HoldersList) -> FilesList:
        """Fetches the blurred version of each par in the given list."""

        return [img.blurred for img in images]


    def safes_blurred(self) -> FilesList:
        """Retrieves the blurred versions of the safe images."""

        return self._load_blurred(self._safes)


    def mines_blurred(self) -> FilesList:
        """Retrieves the blurred versions of the ChubMines."""

        return self._load_blurred(self._mines)


    def shuffled(self, numbers: bool=True) -> FilesList:
        """Generates a shuffled list of the blurred images.
        
        Args:
            numbers: Wether to draw numbers on each image.

        Returns:
            A list of all the blurred images, safe or mine, in a random order.
        """

        all_holders = self.safes + self.mines
        shuffle(all_holders)

        if not numbers:
            return self._load_blurred(all_holders)

        return [holder.blurred_copy_with_number(i) for i, holder in enumerate(all_holders, 1)]
