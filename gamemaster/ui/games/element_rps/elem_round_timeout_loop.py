# from typing import TYPE_CHECKING

# from discord.ext.tasks import Loop
# from discord.utils import MISSING

# if TYPE_CHECKING:
#     from .element_rps_view import ElementRPSView

# _SECONDS_BETWEEN_ITERATIONS: float = 1.0

# class RPSRoundTimeoutLoop(Loop):
#     def __init__(self, iterations: int, base_view):
#         super().__init__(coro,
#                          seconds=_SECONDS_BETWEEN_ITERATIONS,
#                          hours=MISSING,
#                          minutes=MISSING,
#                          time=MISSING,
#                          count=iterations,
#                          reconnect=None,
#                          name=None)

