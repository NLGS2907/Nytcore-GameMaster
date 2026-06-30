from typing import TYPE_CHECKING

from ...tasks.loops import BackgroundLoop

if TYPE_CHECKING:
    from ..players import ConfirmationView  # noqa: F401


class ConfirmationCountdownLoop(BackgroundLoop["ConfirmationView"]):
    async def loop_callback(self):
        if self.is_being_cancelled():
            return

        self.parent_view.change_countdown_msg(self.remaining_loops)
        await self.parent_view.refresh()


    async def before_loop_hook(self):
        self.parent_view.change_countdown_msg(self.count)
        await self.parent_view.refresh()


    async def after_loop_hook(self):
        self.parent_view.change_countdown_msg(None)
        if self.is_being_cancelled():
            await self.parent_view.refresh()
            return

        game_view = self.parent_view.manager.assemble_view(self.parent_view.user,
                                                           self.parent_view.parent_msg,
                                                           self.parent_view.user)
        await game_view.reset()
        await self.parent_view.parent_msg.edit(view=game_view)