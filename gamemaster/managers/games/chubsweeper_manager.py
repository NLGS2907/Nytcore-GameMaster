from typing import TYPE_CHECKING

from ...games import ChubSweeperGame, ChubSweeperOptions
from ...ui.games.chubsweeper import ChubSweeperOptionsModal, ChubSweeperView
from ..game_manager import GameManager

if TYPE_CHECKING:
    from ...games import BaseGame, BaseOptions
    from ...ui.games.game_view_base import BaseGameView
    from ...ui.games.options_modal_base import BaseOptionsModal
    from ..game_manager import GameID


class ChubSweeperManager(GameManager):
    """Class that manages the game of Element Rock-Paper-Scissors."""

    @staticmethod
    def game_id() -> "GameID":
        return 20260701190551


    @staticmethod
    def game_class() -> type["BaseGame"]:
        return ChubSweeperGame


    @staticmethod
    def options_class() -> type["BaseOptions"]:
        return ChubSweeperOptions


    @staticmethod
    def view_class() -> type["BaseGameView"]:
        return ChubSweeperView


    @staticmethod
    def options_modal_class() -> type["BaseOptionsModal"]:
        return ChubSweeperOptionsModal