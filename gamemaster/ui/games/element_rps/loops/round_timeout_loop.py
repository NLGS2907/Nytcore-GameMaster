from typing import TYPE_CHECKING

from .....tasks.loops import BackgroundLoop

if TYPE_CHECKING:
    from ..element_rps_view import ElementRPSView  # noqa: F401


class RoundTimeoutLoop(BackgroundLoop["ElementRPSView"]):
    async def loop_callback(self):
        if self.is_being_cancelled():
            return

        self.parent_view.set_round_timeout_msg(self.remaining_loops)
        await self.parent_view.refresh()


    async def before_loop_hook(self):
        self.parent_view.set_round_timeout_msg(self.count)
        await self.parent_view.refresh()


    async def after_loop_hook(self):
        self.parent_view.set_round_timeout_msg(None)
        if self.is_being_cancelled():
            await self.parent_view.refresh()
            return

        if not self.parent_view.reveal.is_running():
            self.parent_view.reveal.start()