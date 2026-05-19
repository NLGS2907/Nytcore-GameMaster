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


class EnvManager:
    """Object that manages enviroment vars.
    
    It can read from files and load them later.
    """

    @staticmethod
    def env_path():
        bot_mode = getenv("BOT_MODE", "test").lower()
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
                key, value = line.strip().split(ENV_SEP, 1)
                sanitized_value = value.strip().strip("\"'")
                manager.add_env(key, sanitized_value)

        return manager


    def __init__(self):
        # Do note that this is NOT what the program will be using, just a cached copy,
        # ready to be uploaded.
        self.__stored_envs: EnvDict = {}


    def add_env(self, key: EnvKey, value: EnvVal, overwrite: bool=True) -> None:
        """Adds a new enviroment variable to the internal registry.
        
        Args:
            key: A string to use as hashable key.
            value: A string to be used as value tied to the key.
            overwrite: Wether to replace the env var if an entry with the same key already exists.
        """
        if not overwrite:
            return

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
