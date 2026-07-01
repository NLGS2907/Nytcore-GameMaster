from typing import TYPE_CHECKING

from .....tasks.loops import BackgroundLoop

if TYPE_CHECKING:
    from ..element_rps_view import ElementRPSView  # noqa: F401

NULL_ROUNDS_TOLERANCE: int = 3


class RevealLoop(BackgroundLoop["ElementRPSView"]):
    async def loop_callback(self):
        if self.is_being_cancelled():
            return

        self.parent_view.set_reveal_msg(self.remaining_loops)
        await self.parent_view.refresh()


    async def before_loop_hook(self):
        self.parent_view.set_reveal_msg(self.count)
        await self.parent_view.refresh()


    async def after_loop_hook(self):
        self.parent_view.set_reveal_msg(None)
        if self.is_being_cancelled():
            await self.parent_view.refresh()
            return

        self.parent_view.game.resolve()
        if self.parent_view.game.last_null_rounds(NULL_ROUNDS_TOLERANCE):
            cancel_reason = (f"Neither player has played in the last {NULL_ROUNDS_TOLERANCE} "
                             "rounds, so they were both considered AFK.")
            await self.parent_view.cancel_game(title="Element Rock-Paper-Scissors Canceled",
                                               reason=cancel_reason)
            return

        if not self.parent_view.next_round.is_running():
            # this loop already refreshes the view
            self.parent_view.next_round.start()