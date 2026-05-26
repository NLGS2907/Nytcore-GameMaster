from typing import TYPE_CHECKING, TypeAlias, Union

from ...models import ElementType, RPSRoundResult

if TYPE_CHECKING:
    from discord import Emoji, PartialEmoji

    from ...models import RPSResult

MaybeEmoji: TypeAlias = Union["Emoji", "PartialEmoji"]
EmojiCounter: TypeAlias = dict[ElementType, list[int]]


class RPSResultStats:
    """Helper class for calculating some stats from a finished game of Element RPS."""

    def __init__(self, records: "RPSResult"):
        """Initialize the stats.
        
        Args:
            records: The records to process the stas from.
        """

        self.ties_count: int = 0
        self.player_1_favs: list[MaybeEmoji] = []
        self.player_2_favs: list[MaybeEmoji] = []
        
        self.process(records)


    def _initialize_emoji_counter(self) -> EmojiCounter:
        """Generates an empty emoji counter."""

        return {element: [0, 0] for element in ElementType}


    def process(self, records: "RPSResult"):
        """Process the stats with the given records."""

        emojis_counter = self._initialize_emoji_counter()

        for round in records.walk_rounds():
            if round.result == RPSRoundResult.TIE:
                self.ties_count += 1

            emojis_counter[round.player_1_choice][0] += 1
            emojis_counter[round.player_2_choice][1] += 1

        max_count_player_1 = max(*emojis_counter.values(), key=lambda count: count[0])[0]
        max_count_player_2 = max(*emojis_counter.values(), key=lambda count: count[1])[1]

        self.player_1_favs.extend(elem for elem, elem_count in emojis_counter.items()
                                  if elem_count[0] == max_count_player_1)
        self.player_2_favs.extend(elem for elem, elem_count in emojis_counter.items()
                                  if elem_count[1] == max_count_player_2)
