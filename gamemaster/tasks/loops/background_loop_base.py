from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence, Union

from discord.ext.tasks import Loop
from discord.utils import MISSING

_SECONDS_BETWEEN_ITERATIONS: float = 1.0


class BackgroundLoop[ViewType](Loop, ABC):
    """Background task loop base class.

    All the attributes, aside from the parent view, are already documented in the parent class.
    
    Attributes:
        parent_view: The parent UI View where this loop is attached to.
    """
    def __init__(self,
                *,
                parent_view: ViewType,
                seconds: float=_SECONDS_BETWEEN_ITERATIONS,
                minutes: float=MISSING,
                hours: float=MISSING,
                time: Union[datetime.time, Sequence[datetime.time]]=MISSING,
                count: Optional[int]=None,
                reconnect: bool=True,
                name: Optional[str]=None):
        """Initializes the background loop.

        All the remaining arguments, aside from the parent view, are already documented
        in the parent class.

        Args:
            parent_view: The parent UI View where this loop is attached to.
        """

        super().__init__(self.loop_callback,
                         seconds=seconds,
                         hours=hours,
                         minutes=minutes,
                         time=time,
                         count=count,
                         reconnect=reconnect,
                         name=name)
        self.parent_view: ViewType = parent_view

        self.before_loop(self.before_loop_hook)
        self.after_loop(self.after_loop_hook)


    @abstractmethod
    async def loop_callback(self):
        """Coroutine to call on every loop iteration."""

        raise NotImplementedError


    async def before_loop_hook(self):
        """Hook for logic that runs before the loop starts.
        
        The default implementation does nothing.
        """

        return


    async def after_loop_hook(self):
        """Hook for logic that runs when the loop is halted, canceled, or finishes normally.
        
        The default implementation does nothing.
        """

        return
