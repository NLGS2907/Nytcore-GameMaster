"""Main module for the application.

Can be triggered manually, but is mainly designed to be called from the package entrypoint.
"""

from os import getenv
from sys import argv

from .logger import get_gamemaster_logger
from .gamemaster import GameMaster


def main(*args: str) -> int:
    "Main function."

    sep = "=" * 25
    get_gamemaster_logger().info(f"{sep} Initializing GameMaster {sep}")

    GameMaster(
        verbose=("-v" in args or "--verbose" in args)
    ).run(getenv("TOKEN"), log_handler=None) # The handler was manually set up beforehand

    return 0


if __name__ == "__main__":
    main(*argv)
