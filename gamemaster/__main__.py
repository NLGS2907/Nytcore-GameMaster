"""Entrypoint for the main bot package."""

from os import getenv
from sys import argv

from .env import EnvManager

# We must load env vars before anything else, even before imports.
env_path = getenv("ENV_PATH") or "test.env"
EnvManager.read_from_file(env_path).and_load()

from .main import main  # noqa: E402

if __name__ == "__main__":
    main(*argv)