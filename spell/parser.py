"""A parser to parse the python file (only) to extract docstring and inline comments"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EXAMPLE_DIR = Path.cwd().parent / "examples" / "2.py"


@dataclass
class BaseComment:
    comment: str | None
    line_no: int

    def clean(self, strip_hash: bool = False) -> "BaseComment":
        if not self.comment:
            return self

        _comment: str = self.comment.strip()
        if strip_hash:
            _comment = _comment.strip("#")

        return BaseComment(comment=_comment.strip(), line_no=self.line_no)

    def remove_symbols(self) -> "BaseComment":
        raise NotImplementedError("Not implemented")


@dataclass
class DocstringMetadata:
    cls_name: str | None
    line_no: int | None
    end_line_no: int | None
    col_offset: int | None


@dataclass
class BaseDocstring:
    docstring: str | None
    metadata: DocstringMetadata | None


class FileParser:
    def __init__(self, file: Path):
        self._file = file

    def parse(self) -> None:
        """Parse a python file"""
        self._file_text: str = self._file.read_text()

    def read(self) -> Any:
        """Returns whole file as a string"""
        return self._file.read_text()

    def to_ast(self) -> ast.Module:
        """Convert to ast nodes"""
        return ast.parse(self._file_text)

    def find_docstrings(self, verbose: bool = False) -> list[BaseDocstring]:
        """Return a list of docstring found in functions, methods and module"""

        docstrings: list[BaseDocstring] = []

        nodes: ast.Module = self.to_ast()
        docstrings_ast = (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.Module)
        docstrings_cls = [f for f in ast.walk(nodes) if isinstance(f, docstrings_ast)]

        print(docstrings_cls)

        for cls in docstrings_cls:
            name: str | None = None
            line_no: int | None = None
            end_line_no: int | None = None
            col_offset: int | None = None
            # end_col_offset: int | None = None
            docstring: str | None = ast.get_docstring(cls)

            if not isinstance(cls, ast.Module):
                for node in cls.body:
                    if isinstance(node, ast.Expr):
                        name = cls.name
                        line_no = node.lineno
                        end_line_no = node.end_lineno
                        col_offset = node.col_offset
                        # break  # Fixme: Add break to optimize little bit

            metadata = DocstringMetadata(
                cls_name=name, line_no=line_no, end_line_no=end_line_no, col_offset=col_offset
            )
            docstrings.append(ds := BaseDocstring(docstring=docstring, metadata=metadata))

            if verbose:
                print("-" * 100)
                print(f"class: {ast.dump(cls)}", end="\n\n")
                print(ds.metadata, end="\n\n")
                print(ds.docstring)
                print("-" * 100, end="\n\n")

        return docstrings

    def find_inline_comments(self) -> list[BaseComment]:
        """Returns a list inline comments i.e. comments starts with '#'"""
        lines = self._file_text.splitlines()
        comments: list[BaseComment] = []

        for idx, line in enumerate(lines, start=1):
            comment = line.strip().startswith("#")
            if comment:
                comments.append(BaseComment(line, idx))
        return comments


def main() -> None:
    parser = FileParser(EXAMPLE_DIR)
    parser.parse()
    parser.find_docstrings(verbose=True)
    for comment in parser.find_inline_comments():
        print(comment)
        print(comment.clean())
        print(comment.clean(strip_hash=True), end="\n\n")


if __name__ == "__main__":
    main()
