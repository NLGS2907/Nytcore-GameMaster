"""Main module for the application.

Can be triggered manually, but is mainly designed to be called from the package entrypoint.
"""

from asyncio import Runner, SelectorEventLoop, new_event_loop, set_event_loop
from os import getenv
from platform import system
from sys import argv
from typing import TYPE_CHECKING

from .arg_parser import BotArgParser
from .gamemaster import GameMaster
from .logger import get_gamemaster_logger, log_lvl

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop


def create_event_loop() -> "AbstractEventLoop":
    """Generates the event loop factory needed for the asyncio runner."""

    loop = (SelectorEventLoop() if system() == "Windows" else new_event_loop())
    set_event_loop(loop)

    return loop


async def main(*args: str) -> int:
    "Main function."

    flags = BotArgParser().parse_args(args[1:])

    sep = "=" * 25
    get_gamemaster_logger(log_lvl(flags.verbose)).info(f"{sep} Initializing GameMaster {sep}")

    bot = GameMaster(verbose=flags.verbose, only_bot_logger=flags.only_bot)
    async with bot:
        await bot.start(getenv("TOKEN"))

    return 0


if __name__ == "__main__":
    with Runner(loop_factory=create_event_loop) as runner:
        runner.run(main(*argv))
