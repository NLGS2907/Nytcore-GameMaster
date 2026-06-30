from typing import TYPE_CHECKING

from .....tasks.loops import BackgroundLoop

if TYPE_CHECKING:
    from ..element_rps_view import ElementRPSView  # noqa: F401


class NextRoundLoop(BackgroundLoop["ElementRPSView"]):
    async def loop_callback(self):
        if self.is_being_cancelled():
            return

        self.parent_view.set_results_msg(self.remaining_loops)
        await self.parent_view.refresh()


    async def before_loop_hook(self):
        self.parent_view.set_results_msg(self.count)
        await self.parent_view.refresh()


    async def after_loop_hook(self):
        self.parent_view.set_results_msg(None)
        self.parent_view.game.reset_round()

        winner = self.parent_view.game.finished()
        if winner is not None:
            self.parent_view.game.save()
            await self.parent_view.finish_message(winner)
        else:
            self.parent_view.round_timeout.start()
            await self.parent_view.refresh()