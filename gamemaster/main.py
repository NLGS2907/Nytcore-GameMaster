"""Main module for the application.

Can be triggered manually, but is mainly designed to be called from the package entrypoint.
"""

from os import getenv
from sys import argv

from .gamemaster import GameMaster
from .logger import get_gamemaster_logger, log_lvl


def main(*args: str) -> int:
    "Main function."

    sep = "=" * 25
    verbose = ("-v" in args or "--verbose" in args)
    get_gamemaster_logger(log_lvl(verbose)).info(f"{sep} Initializing GameMaster {sep}")

    GameMaster(
        verbose=verbose
    ).run(getenv("TOKEN"), log_handler=None)

    return 0


if __name__ == "__main__":
    main(*argv)
