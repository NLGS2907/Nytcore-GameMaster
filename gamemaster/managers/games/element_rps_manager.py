from typing import TYPE_CHECKING

from ...games import ElementRPSGame, ElementRPSOptions
from ...ui.games.element_rps import ElementRPSOptionsModal, ElementRPSView
from ..game_manager import GameManager

if TYPE_CHECKING:
    from ...games import BaseGame, BaseOptions
    from ...ui.games.game_view_base import BaseGameView
    from ...ui.games.options_modal_base import BaseOptionsModal
    from ..game_manager import GameID


class ElementRPSManager(GameManager):
    """Class that manages the game of Element Rock-Paper-Scissors."""

    @staticmethod
    def game_id() -> "GameID":
        return 20260523151110


    @staticmethod
    def game_class() -> type["BaseGame"]:
        return ElementRPSGame


    @staticmethod
    def options_class() -> type["BaseOptions"]:
        return ElementRPSOptions


    @staticmethod
    def view_class() -> type["BaseGameView"]:
        return ElementRPSView


    @staticmethod
    def options_modal_class() -> type["BaseOptionsModal"]:
        return ElementRPSOptionsModal