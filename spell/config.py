"""The configuration of this project"""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Type, TypeVar

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
