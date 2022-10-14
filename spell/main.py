"""A main entrypoint or command line interface"""

from argparse import ArgumentParser
from pathlib import Path

from spell.config import Config
from spell.parser import FileParser
from spell.walker import Walker


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

    for path in paths:
        print(f"{path.name} : {'+' * 180}")
        file_parser = FileParser(path)
        file_parser.parse()

        doc_strs = file_parser.find_docstrings(verbose=False)
        comments = file_parser.find_inline_comments()

        for c in comments:
            print(c.clean(strip_hash=True))

        for d in doc_strs:
            print(d)


if __name__ == "__main__":
    main()
