from typing import TYPE_CHECKING, Literal, Optional, TypeAlias

from discord import PartialEmoji, SeparatorSpacing
from discord.ui import ActionRow, Container, Separator, TextDisplay

from ....games import ElementRPSGame
from ....models import ElementType
from ..game_view_base import BaseGameView
from .buttons import ElementButton, ElementMapButton
from .loops import NextRoundLoop, RevealLoop, RoundTimeoutLoop

if TYPE_CHECKING:
    from discord import Emoji

    from ....gamemaster import GameMaster
    from ....models import EmojiType, Player
    from ..game_view_base import PossibleMessage, PossibleUser

ElementEmojis: TypeAlias = dict[ElementType, "Emoji"]
StatusMessages: TypeAlias = dict[Literal["reveal", "results", "timeout"], Optional[str]]

SECS_UNTIL_REVEAL: int = 5
SECS_UNTIL_NEXT_ROUND: int = 10

REVEAL_NAME: str = "reveal"
RESULTS_NAME: str = "results"
TIMEOUT_NAME: str = "timeout"


class ElementRPSView(BaseGameView[ElementRPSGame]):
    """Game view for Element Rock-Paper-Scissors."""

    def __init__(self,
                 bot: "GameMaster",
                 parent_msg: "PossibleMessage",
                 origin_user: "PossibleUser",
                 game: ElementRPSGame,
                 *,
                 timeout: Optional[float]=None):
        super().__init__(bot, parent_msg, origin_user, game, timeout=timeout)
        self.player_1: "Player" = self.game.players[0]
        self.player_2: "Player" = self.game.players[1]

        self._emojis = self.load_emojis(hex=self.game.options.use_hex_emojis)
        self._element_buttons: list[ElementButton] = [
            ElementButton(self, element, elem_emoji)
            for element, elem_emoji in self._emojis.items()
        ]
        self._elem_map_btn: ElementMapButton = ElementMapButton(self)

        self._status_msg: StatusMessages = {REVEAL_NAME: None,
                                            RESULTS_NAME: None,
                                            TIMEOUT_NAME: None}

        self.reveal: RevealLoop = RevealLoop(parent_view=self, count=SECS_UNTIL_REVEAL)
        self.next_round: NextRoundLoop = NextRoundLoop(parent_view=self,
                                                       count=SECS_UNTIL_NEXT_ROUND)
        self.round_timeout: RoundTimeoutLoop = RoundTimeoutLoop(
            parent_view=self, count=self.game.options.round_timeout
        )

        self.round_timeout.start()


    async def reset(self):
        container = Container()

        cur_round = self.game.current_round + 1
        if not self.game.round_finished:
            container.add_item(TextDisplay(f"## {self.player_1.username}  VS  "
                                            f"{self.player_2.username}  (Round {cur_round})"))
            reveal_msg = self._status_msg[REVEAL_NAME]
            if reveal_msg is not None:
                container.add_item(Separator(spacing=SeparatorSpacing.small))
                container.add_item(TextDisplay(reveal_msg))

            container.add_item(Separator(spacing=SeparatorSpacing.small))
            container.add_item(ActionRow(self._elem_map_btn))

            timeout_msg = self._status_msg[TIMEOUT_NAME]
            if timeout_msg is not None:
                container.add_item(Separator(spacing=SeparatorSpacing.small))
                container.add_item(TextDisplay(timeout_msg))

            self.add_item(container)

            self.add_item(ActionRow(*self._element_buttons))
            return

        last_result = self.game.last_record()
        player_1_emoji = (self._emojis[last_result.player_1_choice]
                          if last_result.player_1_choice is not None else "_N/A_")
        player_2_emoji = (self._emojis[last_result.player_2_choice]
                          if last_result.player_2_choice is not None else "_N/A_")
        container.add_item(TextDisplay(
            (f"## {self.player_1.username}  {player_1_emoji}\t-\t"
             f"{player_2_emoji}  {self.player_2.username}")
        ))

        winner = self.game.determine_winner(last_result)
        win_msg = (f"{winner.username} has won round {cur_round}!"
                   if winner is not None else f"_Round {cur_round} has ended in a tie._")
        container.add_item(TextDisplay(f"### {win_msg}"))

        player_1_score, player_2_score = self.game.get_scores()
        container.add_item(TextDisplay(f"Current results:\t\t**{player_1_score} - "
                                       f"{player_2_score}**"))

        results_msg = self._status_msg[RESULTS_NAME]
        if results_msg is not None:
            container.add_item(Separator(spacing=SeparatorSpacing.small))
            container.add_item(TextDisplay(f"-# _{results_msg}_"))

        self.add_item(container)


    async def finish_message(self, winner: "Player"):
        """Shows one last message for closing the game.
        
        Args:
            winner: The player that has won, so we don't fetch it again.
        """

        self.clear_items()

        player_1_score, player_2_score = self.game.get_scores()
        stats = self.game.process_stats()

        container = Container(
            TextDisplay(f"## Winner:\t{winner.username}"),
            TextDisplay(f"They have won with a result of **{player_1_score} - {player_2_score}** "
                        f"and **{stats.ties_count} ties**."),
            Separator(spacing=SeparatorSpacing.small),
            TextDisplay(f"-# Favourite elements of **{self.game.player_1.username}**:\t"
                        f"{' ,  '.join(str(self._emojis[fav]) for fav in stats.player_1_favs)}"),
            TextDisplay(f"-# Favourite elements of **{self.game.player_2.username}**:\t"
                        f"{' ,  '.join(str(self._emojis[fav]) for fav in stats.player_2_favs)}")
        )

        self.add_item(container)
        await self.refresh_parent_msg() # because this method does not go through refresh
        self.stop()


    def _load_emoji(self, emoji_name: str, default: "EmojiType", hex: bool=False) -> "Emoji":
        """Loads a single emoji.
        
        If it doesn't find it, returns the default one.

        Args:
            emoji_name: The name of the emoji to search for.
            default: The default emoji to return.
            hex: Wether to use the hexagon versions of the element emojis.

        Returns:
            The Emoji object, ready to use.
        """

        final_name = f"{emoji_name}{'_hex' if hex else ''}"
        return self.bot.emojis.get(final_name, PartialEmoji.from_str(default))


    def load_emojis(self, hex: bool=False) -> ElementEmojis:
        """Loads all the emojis into a dict for later use.
        
        Args:
            hex: Wether to use the hexagon versions of the element emojis.

        Returns:
            The dictionary with the emojis, ready to use.
        """

        return {
            ElementType.FIRE: self._load_emoji("fire", self.game.fire_emoji(), hex),
            ElementType.WIND: self._load_emoji("wind", self.game.wind_emoji(), hex),
            ElementType.IRON: self._load_emoji("iron", self.game.iron_emoji(), hex),
            ElementType.ELECTRIC: self._load_emoji("electric", self.game.electric_emoji(), hex),
            ElementType.WATER: self._load_emoji("water", self.game.water_emoji(), hex)
        }


    def set_reveal_msg(self, remaining_loops: Optional[int]):
        """Generates the current reveal message given the number of remaining loops."""

        msg = (f"All players have made their choice. **Revealing results in {remaining_loops}...**"
               if remaining_loops is not None else None)
        self._status_msg[REVEAL_NAME] = msg


    def set_results_msg(self, remaining_loops: Optional[int]):
        """Generates the current results message given the number of remaining loops."""

        candidate = (f"Beginning next round in {remaining_loops}..."
                     if self.game.finished() is None
                     else f"Game finished! Generating results in {remaining_loops}...")
        msg = (candidate if remaining_loops is not None else None)
        self._status_msg[RESULTS_NAME] = msg


    def set_round_timeout_msg(self, remaining_loops: Optional[int]):
        """Generates the current round timeout message given the number of remaining loops."""

        msg = ((f"-# If both players don't decide in {remaining_loops} seconds, "
                "the round will end on its own.") if remaining_loops is not None else None)
        self._status_msg[TIMEOUT_NAME] = msg
