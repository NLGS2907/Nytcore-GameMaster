from typing import TYPE_CHECKING, Optional, TypeAlias, TypedDict

from ...models import ElementType
from ..game_base import BaseGame
from .element_rps_options import ElementRPSOptions

if TYPE_CHECKING:
    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...models import EmojiType, Player
    from ..game_base import EmojisCollection

WeaknessMap: TypeAlias = dict[ElementType, ElementType]

# TODO: Replace this for a more persistent model ASAP!!!!
class _RoundResultRecord(TypedDict):
    player_1_choice: ElementType
    player_2_choice: ElementType
    who_won: Optional["Player"]

WEAKNESSES: WeaknessMap = {
    ElementType.WIND: ElementType.FIRE,
    ElementType.IRON: ElementType.WIND,
    ElementType.ELECTRIC: ElementType.IRON,
    ElementType.WATER: ElementType.ELECTRIC,
    ElementType.FIRE: ElementType.WATER
}


class ElementRPSGame(BaseGame[ElementRPSOptions]):
    """Game class for a game of Element Rock-Paper-Scissors.

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
                 options: ElementRPSOptions):
        super().__init__(bot, host_user, players, options=options)

        self._player_1_choice: Optional[ElementType] = None
        self._player_2_choice: Optional[ElementType] = None

        self._player_1_score: int = 0
        self._player_2_score: int = 0

        self._cur_round: int = 0
        self._round_finished: bool = False
        self.__records: list[_RoundResultRecord] = [] # TODO: Replace this for a more persistent model ASAP!!!!


    @staticmethod
    def title_name() -> str:
        return "Element Rock-Paper-Scissors"


    @staticmethod
    def description() -> Optional[str]:
        return "Classic game of Rock-Paper-Scissors, but with NIKKE's element codes!"


    @staticmethod
    def emojis_collection() -> "EmojisCollection":
        return [__class__.wind_emoji(),
                __class__.water_emoji(),
                __class__.iron_emoji(),
                __class__.fire_emoji(),
                __class__.electric_emoji()]


    @staticmethod
    def minimum_players() -> int:
        return 2


    @staticmethod
    def maximum_players() -> int:
        return 2


    @staticmethod
    def wind_emoji() -> "EmojiType":
        """Returns the game's fallback emoji for the wind element."""

        return "💨"

    @staticmethod
    def water_emoji() -> "EmojiType":
        """Returns the game's fallback emoji for the water element."""

        return "💦"

    @staticmethod
    def iron_emoji() -> "EmojiType":
        """Returns the game's fallback emoji for the iron element."""

        return "🔩" # close enough

    @staticmethod
    def fire_emoji() -> "EmojiType":
        """Returns the game's fallback emoji for the fire element."""

        return "🔥"

    @staticmethod
    def electric_emoji() -> "EmojiType":
        """Returns the game's fallback emoji for the electric element."""

        return "⚡"


    @property
    def current_round(self) -> int:
        """Returns the number of the ucrrent round being played."""

        return self._cur_round


    @property
    def round_finished(self) -> bool:
        """Tells if the ucrrent round has finished playing."""

        return self._round_finished


    def weak_against(self, elem_1: ElementType, elem_2: ElementType) -> bool:
        """Checks if `elem_1` is weak against `elem_2`."""

        return elem_2 == WEAKNESSES[elem_1]


    def reset_choices(self):
        """Reset the choices of the players, so that a new round may begin."""

        self._player_1_choice = None
        self._player_2_choice = None


    def make_choice(self, choice: ElementType, is_player_1: bool):
        """Makes a choice and registers it.

        Args:
            choice: The element chosen.
            is_player_1: If `True`, registers the choice of player 1. If `False`, it registers
                         it under the name of `player_2`.
        """

        if is_player_1:
            self._player_1_choice = choice
        else:
            self._player_2_choice = choice


    def has_made_choice(self, is_player_1: bool) -> bool:
        """Checks if a player has already made a choice.
        
        Args:
            is_player_1: If `True`, registers the choice of player 1. If `False`, it registers
                         it under the name of `player_2`.
        """

        return (self._player_1_choice if is_player_1 else self._player_2_choice) is not None


    def choices_made(self) -> bool:
        """Checks if both the players have made choices."""

        return self._player_1_choice is not None and self._player_2_choice is not None


    def get_choices(self) -> tuple[Optional[ElementType], Optional[ElementType]]:
        """Retrieves the choices made for both the players."""

        return self._player_1_choice, self._player_2_choice


    def get_scores(self) -> tuple[int, int]:
        """Gets the scores of both players."""

        return self._player_1_score, self._player_2_score


    def last_record(self) -> Optional[_RoundResultRecord]:
        """Returns the records of the last round"""

        if not self.__records:
            return None

        return self.__records[self._cur_round]


    def resolve(self):
        """Closes off the round and tells the results."""

        self._round_finished = True
        round_winner = None

        if self.weak_against(self._player_2_choice, self._player_1_choice):
            round_winner = self.players[0] # player 1 won
            self._player_1_score += 1
        elif self.weak_against(self._player_1_choice, self._player_2_choice):
            round_winner = self.players[1] # player 2 won
            self._player_2_score += 1

        self.__records.append(dict(player_1_choice=self._player_1_choice,
                                   player_2_choice=self._player_2_choice,
                                   who_won=round_winner))



    def reset_round(self):
        """Resets the parameters for another round."""

        self._cur_round += 1
        self._round_finished = False

        self._player_1_choice = None
        self._player_2_choice = None
