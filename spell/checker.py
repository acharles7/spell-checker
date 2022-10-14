"""A checker to inspect docstring and inline comments"""
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Generator, Type, TypeVar

_T = TypeVar("_T")


@dataclass
class Config:

    paths: list[Path]
    verbosity: int
    config_file: str | None = None
    dump_config: bool = False
    include: list[Path] | None = None
    exclude: list[Path] | None = None

    @classmethod
    def from_argparser(cls: Type[_T], parser: ArgumentParser) -> _T:
        args: Namespace = parser.parse_args()
        config: dict[str, Any] = {}

        for field in fields(cls):
            if hasattr(args, field.name):
                config[field.name] = getattr(args, field.name)
        return cls(**config)


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
