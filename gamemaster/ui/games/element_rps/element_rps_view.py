from discord.ui import TextDisplay

from ....games import ElementRPSGame
from ..game_view_base import BaseGameView


class ElementRPSView(BaseGameView[ElementRPSGame]):
    """Game view for Element Rock-Paper-Scissors."""

    placeholder = TextDisplay("Playing RPS!")