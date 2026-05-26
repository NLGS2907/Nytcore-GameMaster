from datetime import datetime
from typing import TYPE_CHECKING, Optional, TypeAlias

from ...models import ElementType, RPSResult, RPSRoundResult
from ..game_base import BaseGame
from .element_rps_options import ElementRPSOptions
from .result_stats import RPSResultStats

if TYPE_CHECKING:
    from discord.abc import User

    from ...gamemaster import GameMaster
    from ...models import EmojiType, Player, RPSRoundData
    from ..game_base import EmojisCollection

WeaknessMap: TypeAlias = dict[ElementType, ElementType]

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
        self.__results: RPSResult = RPSResult(None, self.players[0], self.players[1], [],
                                              datetime.now())


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


    @property
    def player_1(self) -> "Player":
        """Returns the first player of the pair."""

        return self.players[0]


    @property
    def player_2(self) -> "Player":
        """Returns the second player of the pair."""

        return self.players[1]


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


    def last_record(self) -> Optional["RPSRoundData"]:
        """Returns the records of the last round"""

        return self.__results.last_round()


    def determine_winner(self, round_data: "RPSRoundData") -> Optional["Player"]:
        """Determines the winner of the round."""

        return self.__results.determine_winner(round_data)


    def process_stats(self) -> RPSResultStats:
        """Retrieves some stats from the finished game."""

        return RPSResultStats(self.__results)


    def resolve(self):
        """Closes off the round and tells the results."""

        self._round_finished = True
        round_result = RPSRoundResult.TIE

        if self.weak_against(self._player_2_choice, self._player_1_choice):
            round_result = RPSRoundResult.VICTORY
            self._player_1_score += 1
        elif self.weak_against(self._player_1_choice, self._player_2_choice):
            round_result = RPSRoundResult.DEFEAT
            self._player_2_score += 1

        self.__results.add_data(self._player_1_choice, self._player_2_choice, round_result)


    def reset_round(self):
        """Resets the parameters for another round."""

        self._cur_round += 1
        self._round_finished = False

        self._player_1_choice = None
        self._player_2_choice = None


    def enough_points(self, is_player_1: bool) -> bool:
        """Checks if a given player has enough points to have won the game."""

        threshold = self.options.winning_rounds
        return (self._player_1_score if is_player_1 else self._player_2_score) >= threshold


    def finished(self) -> Optional["Player"]:
        """Checks if one of the players reached the required amount of points to win.
        
        Returns:
            The player that has won, or `None` if the game is not finished yet.
        """

        winner = None
        if self.enough_points(True):
            winner = self.player_1
        elif self.enough_points(False):
            winner = self.player_2

        return winner


    def save(self):
        """Saves the record of the game in its repository."""

        self.bot.repositories.rps_result.save(self.__results)
