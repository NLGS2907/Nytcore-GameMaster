"""Entrypoint for the main bot package."""

from asyncio import Runner
from sys import argv

from .env import EnvManager

# We must load env vars before anything else, even before imports.
EnvManager.read_from_file(EnvManager.env_path()).and_load()

from .main import create_event_loop, main  # noqa: E402

if __name__ == "__main__":
    with Runner(loop_factory=create_event_loop) as runner:
        runner.run(main(*argv))