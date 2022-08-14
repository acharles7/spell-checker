from pathlib import Path

from spell.utils import read_file

EXAMPLE_DIR = Path.cwd().parent / "examples" / "1.py"


def main() -> None:
    print("This is python documentation spell checker")

    content = read_file(EXAMPLE_DIR)
    print(content)


if __name__ == "__main__":
    main()
