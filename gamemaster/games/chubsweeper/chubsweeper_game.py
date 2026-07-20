from collections.abc import Iterator
from typing import TYPE_CHECKING, Iterable, Optional, TypeAlias

from ..game_base import BaseGame
from .choice_tracker import ChoiceTracker
from .chubsweeper_options import ChubSweeperOptions
from .img_holder import ImagePairHolder

if TYPE_CHECKING:
    from io import BytesIO

    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...models import Player
    from ..game_base import EmojisCollection
    from .blur_level import BlurLevel
    from .img_choice import ImageChoice

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

        self._cur_round: int = 0
        self._cur_miner_i: Optional[int] = None
        self._choice_tracker: Optional[ChoiceTracker] = None


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


    @property
    def current_round(self) -> int:
        """Retrieves the current round number."""

        return self._cur_round


    @property
    def current_player(self) -> Optional["Player"]:
        """Retrieves the player whose turn it is right now, or `None` if the game didn't start."""

        return (None if self._cur_miner_i is None else self._miners[self._cur_miner_i])


    @property
    def tracker(self) -> Optional[ChoiceTracker]:
        """Retrieves the tracker for the current choices, if available."""

        return self._choice_tracker


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


    def _next_player(self):
        """Advances the current player to the next one in the list."""

        if self._cur_miner_i is None:
            self._cur_miner_i = 0
            return

        self._cur_miner_i = (self._cur_miner_i + 1) % len(self._miners)


    def reset_round(self):
        """Runs the final arrangements just before starting a round."""

        self._cur_round += 1
        self._next_player()
        self._choice_tracker = ChoiceTracker(safes=self._safes, mines=self._mines)


    def current_deck(self) -> FilesList:
        """Retrieves a list of files based on their individual 'uncovered' states."""

        return self._choice_tracker.showable_faces()


    def walk_choices(self) -> Iterator["ImageChoice"]:
        """Yields all the choices of the tracker, in order."""

        if self._choice_tracker is None:
            return

        yield from self._choice_tracker


    def make_choice(self, n: int):
        """Registers a choice with the underlying tracker.

        Args:
            n: The number of the choice to register.

        Returns:
            A boolean value indicating if the player has lost due to this choice.
        """

        return self.tracker.uncover(n)


    def current_score(self) -> int:
        """Retrieves the score of the current player, or zero if the tracker is `None`."""

        if self.tracker is None:
            return 0

        return self.tracker.score
