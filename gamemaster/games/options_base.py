from abc import ABC, abstractmethod
from typing import Self


class BaseOptions(ABC):
    """Base functionalities that an option should have."""

    @classmethod
    @abstractmethod
    def default(self) -> Self:
        """Returns an instance of these options with all values set to their default states."""

        raise NotImplementedError
