"""Main module for the application.

Can be triggered manually, but is mainly designed to be called from the package entrypoint.
"""

from os import getenv
from sys import argv

from .arg_parser import BotArgParser
from .gamemaster import GameMaster
from .logger import get_gamemaster_logger, log_lvl


def main(*args: str) -> int:
    "Main function."

    flags = BotArgParser().parse_args(args[1:])

    sep = "=" * 25
    get_gamemaster_logger(log_lvl(flags.verbose)).info(f"{sep} Initializing GameMaster {sep}")

    GameMaster(
        verbose=flags.verbose,
        only_bot_logger=flags.only_bot
    ).run(getenv("TOKEN"), log_handler=None)

    return 0


if __name__ == "__main__":
    main(*argv)
