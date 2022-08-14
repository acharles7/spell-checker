from pathlib import Path
from typing import Any

EXAMPLE_DIR = Path.cwd().parent / "examples" / "1.py"


class FileParser:
    def __init__(self, file: Path):
        self._file = file

    def read(self) -> Any:
        return self._file.read_text()

    def analyze(self) -> None:
        content = self.read()
        print(content)
        return None


def main() -> None:
    print("This is python documentation spell checker")

    parser = FileParser(EXAMPLE_DIR)
    parser.analyze()


if __name__ == "__main__":
    main()
