"""A walker to retrieve necessary files path"""

from dataclasses import dataclass
from pathlib import Path
from typing import Generator

from spell.config import Config


def find_paths(paths: list[Path]) -> Generator[Path, None, None]:
    """Yields path recursively"""

    for path in paths:
        # print(f"path: {path} | parent: {path.parent}")
        # Fixme: Can use Path.rglob() to find .py file
        # Filter out dot files and cache directories for optimization
        if path.is_file() and path.suffix == ".py":
            yield path
        elif path.is_dir():
            for p in path.iterdir():
                yield from find_paths([p])
        else:
            # print(f"Unnecessary path found: {path}")
            pass


@dataclass
class Walker:
    """A walker class to walk through project directories and fetch required paths"""

    config: Config

    def walk(self) -> list[Path]:
        return [path for path in find_paths(self.config.paths)]
