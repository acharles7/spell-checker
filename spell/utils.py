from pathlib import Path


def read_file(file: Path) -> str:
    return file.read_text()
