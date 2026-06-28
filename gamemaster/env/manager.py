"""Enviroment variables manager.

In essence, it reads, loads and/or saves vars as needed.
"""

from os import environ, getenv
from typing import Self, TypeAlias

FilePath: TypeAlias = str
EnvKey: TypeAlias = str
EnvVal: TypeAlias = str
EnvDict: TypeAlias = dict[EnvKey, EnvVal]

ENV_SEP: str = "="
ENV_EXT: str = ".env"
COMMENT_CHAR: str = "#"
BOT_MODE_ENV: str = "BOT_MODE"


class EnvManager:
    """Object that manages enviroment vars.
    
    It can read from files and load them later.
    """

    @staticmethod
    def env_path():
        bot_mode = getenv(BOT_MODE_ENV, "test").lower()
        return f"./{bot_mode}{ENV_EXT}"


    @classmethod
    def read_from_file(cls, file_path: FilePath) -> Self:
        """Populates the manager using data from a file.
        
        The expected format is something like:
        ```
        <key1>=<val1>
        <key2>=<val2>
        <key3>=<val3>
        ...
        ```
        """

        manager = cls()

        with open(file_path, encoding="utf-8") as env_file:
            for line in env_file:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith(COMMENT_CHAR):
                    continue
                key, value = stripped_line.split(ENV_SEP, 1)
                sanitized_value = value.strip().strip("\"'")
                manager.add_env(key, sanitized_value)

        return manager


    def __init__(self):
        # Do note that this is NOT what the program will be using, just a cached copy,
        # ready to be uploaded.
        self.__stored_envs: EnvDict = {}


    def __len__(self) -> int:
        """Returns how many env vars are loaded in the manager."""

        return len(self.__stored_envs)


    def __contains__(self, env_key: EnvKey) -> bool:
        """Determines if a given env var key is present in the loaded variables."""

        return env_key in self.__stored_envs


    def __getitem__(self, env_key: EnvKey) -> EnvVal:
        """Returns an item from the internal registry of env vars, if it exists.
        
        Raises:
            KeyError: The given env key is not present in the registry.
        """

        return self.__stored_envs[env_key]


    def add_env(self, key: EnvKey, value: EnvVal, overwrite: bool=True) -> None:
        """Adds a new enviroment variable to the internal registry.
        
        Args:
            key: A string to use as hashable key.
            value: A string to be used as value tied to the key.
            overwrite: Wether to replace the env var if an entry with the same key already exists.
        """
        if overwrite:
            self.__stored_envs[key] = value

        self.__stored_envs.setdefault(key, value)


    def and_load(self, overwrite: bool=True) -> None:
        """Loads the internal registry to the actual, global one.
        
        Args:
            overwrite: If `True` and the variable already exists in the enviroment, replace it with
                       the given value; otherwise do nothing. Repeat this for every var in the
                       registry. 
        """

        envs = self.__stored_envs.items()

        if overwrite:
            for key, val in envs:
                environ[key] = val
            return

        for key, val in envs:
            environ.setdefault(key, val)
