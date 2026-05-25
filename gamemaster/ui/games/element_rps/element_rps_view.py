from typing import TYPE_CHECKING, Optional, TypeAlias

from discord import PartialEmoji, SeparatorSpacing
from discord.ext.tasks import loop
from discord.ui import ActionRow, Container, Separator, TextDisplay

from ....games import ElementRPSGame
from ....models import ElementType
from ..game_view_base import BaseGameView
from .elem_map_btn import ElementMapButton
from .element_btn import ElementButton

if TYPE_CHECKING:
    from discord import Emoji

    from ....gamemaster import GameMaster
    from ....models import EmojiType, Player
    from ..game_view_base import PossibleMessage, PossibleUser

ElementEmojis: TypeAlias = dict[ElementType, "Emoji"]

SECS_UNTIL_REVEAL: int = 5
SECS_UNTIL_NEXT_ROUND: int = 10


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

        self._reveal_msg: Optional[str] = None
        self._results_msg: Optional[str] = None


    async def reset(self):
        container = Container()

        cur_round = self.game.current_round + 1
        if not self.game.round_finished:
            container.add_item(TextDisplay(f"## {self.player_1.username}  VS  "
                                            f"{self.player_2.username}  (Round {cur_round})"))
            if self._reveal_msg is not None:
                container.add_item(Separator(spacing=SeparatorSpacing.small))
                container.add_item(TextDisplay(self._reveal_msg))

            container.add_item(Separator(spacing=SeparatorSpacing.small))
            container.add_item(ActionRow(self._elem_map_btn))

            self.add_item(container)

            self.add_item(ActionRow(*self._element_buttons))
            return

        last_result = self.game.last_record()
        container.add_item(TextDisplay(
            (f"## {self.player_1.username}  {self._emojis[last_result["player_1_choice"]]}\t-\t"
             f"{self._emojis[last_result["player_2_choice"]]}  {self.player_2.username}")
        ))

        winner = last_result['who_won']
        win_msg = (f"{winner.username} has won round {cur_round}!"
                   if winner is not None else f"_Round {cur_round} has ended in a tie._")
        container.add_item(TextDisplay(f"### {win_msg}"))

        player_1_score, player_2_score = self.game.get_scores()
        container.add_item(TextDisplay(f"Current results:\t\t**{player_1_score} - "
                                       f"{player_2_score}**"))

        if self._results_msg is not None:
            container.add_item(Separator(spacing=SeparatorSpacing.small))
            container.add_item(TextDisplay(f"-# _{self._results_msg}_"))

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
                        f"{', '.join(str(self._emojis[fav]) for fav in stats.player_1_favs)}"),
            TextDisplay(f"-# Favourite elements of **{self.game.player_2.username}**:\t"
                        f"{', '.join(str(self._emojis[fav]) for fav in stats.player_2_favs)}")
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


    def _generate_reveal_msg(self, current_loop: int) -> str:
        """Generates the current reveal message given the current loop number."""

        return f"All players have made their choice. **Revealing results in {current_loop}...**"


    @loop(seconds=1.0, count=SECS_UNTIL_REVEAL)
    async def reveal(self):
        """Countdown to reveal the results."""

        if self.reveal.is_being_cancelled():
            return

        cur_loop = SECS_UNTIL_REVEAL - self.reveal.current_loop
        self._reveal_msg = self._generate_reveal_msg(cur_loop)
        await self.refresh()


    @reveal.before_loop
    async def before_reveal(self):
        self._reveal_msg = self._generate_reveal_msg(SECS_UNTIL_REVEAL)
        await self.refresh()


    @reveal.after_loop
    async def after_reveal(self):
        self._reveal_msg = None
        if self.reveal.is_being_cancelled():
            await self.refresh()
        else:
            self.game.resolve()
            if not self.next_round.is_running():
                self.next_round.start() # this loop already refreshes the view


    def _generate_results_msg(self, current_loop: int) -> str:
        """Generates the current results message given the current loop number."""

        return (f"Beginning next round in {current_loop}..."
                if self.game.finished() is None
                else f"Game finished! Generating results in {current_loop}...")


    @loop(seconds=1.0, count=SECS_UNTIL_NEXT_ROUND)
    async def next_round(self):
        """Countdown to go to the next round."""

        if self.next_round.is_being_cancelled():
            return

        cur_loop = SECS_UNTIL_NEXT_ROUND - self.next_round.current_loop
        self._results_msg = self._generate_results_msg(cur_loop)
        await self.refresh()


    @next_round.before_loop
    async def before_next_round(self):
        self._results_msg = self._generate_results_msg(SECS_UNTIL_NEXT_ROUND)
        await self.refresh()


    @next_round.after_loop
    async def after_next_round(self):
        self._results_msg = None
        self.game.reset_round()

        winner = self.game.finished()
        if winner is not None:
            await self.finish_message(winner)
        else:
            await self.refresh()
