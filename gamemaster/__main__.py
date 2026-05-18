"""Entrypoint for the main bot package."""

from sys import argv

from .env import EnvManager

# We must load env vars before anything else, even before imports.
EnvManager.read_from_file(EnvManager.env_path).and_load()

from .main import main  # noqa: E402

if __name__ == "__main__":
    main(*argv)