"""Main module for the application.

Can be triggered manually, but is mainly designed to be called from the package entrypoint.
"""

from os import getenv
from sys import argv

# from .db import init_database
# from .logger import AssistLogger
from .gamemaster import GameMaster


def main(*args: str) -> int:
    "Main function."

    GameMaster(
        verbose=("-v" in args or "--verbose" in args)
    ).run(getenv("TOKEN"), log_handler=None) # The handler was manually set up beforehand

    return 0


if __name__ == "__main__":
    main(*argv)
