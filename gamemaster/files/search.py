"""Searching algorithms for directories and other files."""

from pathlib import Path
from typing import Optional


def search_paths(pattern: str="*",
                 path_name: Optional[str]=None,
                 recursive: bool=True,
                 include_files: bool=True,
                 include_dirs: bool=True,
                 ignore_patterns: tuple[str, ...]=()) -> list[str]:
    """Searches through a given directory in search for subdirectory entries.

    Args:
        pattern: Retrieve only entries that are validated by this glob pattern.
        path_name: The path from where to start the search. If not set, then the current
                   working directory is used.
        recursive: Wether to recursively search in the subdirectories too.
        include_files: Wether to include file entries.
        include_dirs: Wether to include directory entries.
        ignore_patterns: Skip any entry that coincides with any given glob pattern on this tuple,
                         regardless of any validation of the other filters.
    """

    ruta = Path(path_name if path_name is not None else ".")

    return list(fpath.as_posix() for fpath in (ruta.rglob(pattern)
                                               if recursive
                                               else ruta.glob(pattern))
                if ((fpath.is_file() if include_files else False
                    or fpath.is_dir() if include_dirs else False)
                    and all(not fpath.match(patr) for patr in ignore_patterns)))


def search_files(pattern: str="*",
                 path_name: Optional[str]=None,
                 recursive: bool=True,
                 ignore_patterns: tuple[str, ...]=()) -> list[str]:
    """Searches through a given directory in search for file entries.

    Args:
        pattern: Retrieve only entries that are validated by this glob pattern.
        path_name: The path from where to start the search. If not set, then the current
                   working directory is used.
        recursive: Wether to recursively search in the subdirectories too.
        ignore_patterns: Skip any entry that coincides with any given glob pattern on this tuple,
                         regardless of any validation of the other filters.
    """

    return search_paths(pattern=pattern,
                        path_name=path_name,
                        recursive=recursive,
                        include_files=True,
                        include_dirs=False,
                        ignore_patterns=ignore_patterns)
