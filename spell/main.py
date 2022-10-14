"""A main entrypoint or command line interface"""

from argparse import ArgumentParser
from pathlib import Path

from spell.checker import Config, Walker


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="The name of a directory (e.g. spell) or file (e.g. spell/parser.py) ",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        action="count",
        default=0,
        help="Verbosity (between 1-2 occurrences with more leading to more verbose logging).",
    )
    parser.add_argument("-c", "--config-file", type=Path, help="Configuration file")
    parser.add_argument("--dump-config", action="store_true", help="Dump configuration and exit")

    config = Config.from_argparser(parser)
    print("Final Config", config)

    walker = Walker(config)
    paths = walker.walk()
    print(paths)


if __name__ == "__main__":
    main()
