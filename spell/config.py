"""The configuration of this project"""

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field, fields
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
    supported_extensions: list[str] = field(default_factory=list)
    suggestions: int = 2

    @classmethod
    def from_argparser(cls: Type[_T], parser: ArgumentParser) -> _T:
        args: Namespace = parser.parse_args()
        config: dict[str, Any] = {}

        for f in fields(cls):
            if hasattr(args, f.name):
                config[f.name] = getattr(args, f.name)
        return cls(**config)
