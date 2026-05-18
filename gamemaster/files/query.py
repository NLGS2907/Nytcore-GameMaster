"""Algorithms for consulting file contents."""

from collections import deque


def tail(path: str, n: int) -> list[str]:
    """Returns the last `n` lines in a file.
    
    Args:
        path: The path of the file to tail.
        n: The amount of lines to retrieve.
    """

    lines = []
    with open(path, mode="r", encoding="utf-8") as file:
        lines.extend(deque(file, n))

    return lines
