"""A parser to parse the python file (only) to extract docstring and inline comments"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spell.types import CommentType, Text

EXAMPLE_DIR = Path.cwd().parent / "examples" / "1.py"


@dataclass
class BaseComment:
    comment: str | None
    line_no: int
    ignore: bool = False
    _type: CommentType = CommentType.INLINE

    def clean(self, strip_hash: bool = False) -> "BaseComment":
        if not self.comment:
            return self

        _comment: str = self.comment.strip()
        if strip_hash:
            _comment = _comment.strip("#").strip()
        return BaseComment(comment=_comment, line_no=self.line_no)

    def is_code(self) -> bool:
        """Returns True if commented line is python code"""
        assert self.comment is not None
        try:
            ast.parse(self.comment)
        except SyntaxError:
            return False
        return True

    @property
    def text(self) -> Text:
        assert self.comment is not None
        return Text(self.comment)


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
    _type: CommentType
    # TODO: Add identifier to identify where docstring came from i.e. Enum.Module, Enum.Function etc.

    @property
    def text(self) -> Text:
        assert self.docstring is not None
        return Text(self.docstring)


class Parser:
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
            _type: CommentType
            docstring: str | None = ast.get_docstring(cls)

            # if no docstring found then ignore it
            if not docstring:
                continue

            match cls:
                case ast.Module():
                    _type = CommentType.MODULE
                case ast.ClassDef():
                    _type = CommentType.CLASS
                case ast.FunctionDef() | ast.AsyncFunctionDef():
                    _type = CommentType.FUNCTION
                case _:
                    raise Exception(f"Unhandled class found: {cls}")

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
            docstrings.append(ds := BaseDocstring(docstring=docstring, metadata=metadata, _type=_type))

            if verbose:
                print("-" * 100)
                print(f"class: {ast.dump(cls)}", end="\n\n")
                print(ds.metadata, end="\n\n")
                print(ds.docstring)
                print(ds._type)
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
    parser = Parser(EXAMPLE_DIR)
    parser.parse()
    ds = parser.find_docstrings(verbose=True)
    for d in ds:
        print(d)
    for comment in parser.find_inline_comments():
        print(comment)
        print(comment.clean())
        print(comment.clean(strip_hash=True), end="\n\n")


if __name__ == "__main__":
    main()
