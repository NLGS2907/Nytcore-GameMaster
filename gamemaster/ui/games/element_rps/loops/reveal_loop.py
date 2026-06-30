from typing import TYPE_CHECKING

from .....tasks.loops import BackgroundLoop

if TYPE_CHECKING:
    from ..element_rps_view import ElementRPSView  # noqa: F401


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
        else:
            self.parent_view.game.resolve()
            if not self.parent_view.next_round.is_running():
                # this loop already refreshes the view
                self.parent_view.next_round.start()