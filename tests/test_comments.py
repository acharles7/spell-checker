from pathlib import Path
from unittest import TestCase

from spell.parser import BaseComment, BaseDocstring, DocstringMetadata, Parser
from spell.types import CommentType


class TestInlineComments(TestCase):

    file = Path(__file__).parent / "data" / "file1.py"
    parser = Parser(file)
    parser.parse()

    actual_comments = parser.find_inline_comments()

    def test_inline_comments(self) -> None:
        expected_comments = [
            BaseComment(comment="        # convert str to int", line_no=18, _type=CommentType.INLINE),
            BaseComment(comment="        # convert to str & then int", line_no=21, _type=CommentType.INLINE),
            BaseComment(comment="        # try to cast to int", line_no=24, _type=CommentType.INLINE),
        ]
        for a, b in zip(self.actual_comments, expected_comments):
            assert a.comment == b.comment

    def test_inline_comments_cleaned(self) -> None:
        expected_comments = [
            BaseComment(comment="# convert str to int", line_no=18, _type=CommentType.INLINE),
            BaseComment(comment="# convert to str & then int", line_no=21, _type=CommentType.INLINE),
            BaseComment(comment="# try to cast to int", line_no=24, _type=CommentType.INLINE),
        ]
        for a, b in zip(self.actual_comments, expected_comments):
            assert a.clean() == b

    def test_inline_comments_stripped(self) -> None:
        expected_comments = [
            BaseComment(comment="convert str to int", line_no=18, _type=CommentType.INLINE),
            BaseComment(comment="convert to str & then int", line_no=21, _type=CommentType.INLINE),
            BaseComment(comment="try to cast to int", line_no=24, _type=CommentType.INLINE),
        ]
        for a, b in zip(self.actual_comments, expected_comments):
            assert a.clean(strip_hash=True) == b


class TestDocstrings(TestCase):

    file = Path(__file__).parent / "data" / "file1.py"
    parser = Parser(file)
    parser.parse()

    actual_docstrings = parser.find_docstrings()

    def test_docstrings(self) -> None:
        expected_docstrings = [
            BaseDocstring(
                docstring="A python test file",
                metadata=DocstringMetadata(cls_name=None, line_no=None, end_line_no=None, col_offset=None),
                _type=CommentType.MODULE,
            ),
            BaseDocstring(
                docstring="Returns 'hello'",
                metadata=DocstringMetadata(cls_name="hello", line_no=6, end_line_no=6, col_offset=4),
                _type=CommentType.FUNCTION,
            ),
            BaseDocstring(
                docstring="A class represents foo and bar",
                metadata=DocstringMetadata(cls_name="Converter", line_no=11, end_line_no=11, col_offset=4),
                _type=CommentType.CLASS,
            ),
            BaseDocstring(
                docstring="Converts to integer representation",
                metadata=DocstringMetadata(cls_name="convert", line_no=17, end_line_no=17, col_offset=8),
                _type=CommentType.FUNCTION,
            ),
        ]
        for a, b in zip(self.actual_docstrings, expected_docstrings):
            assert a == b
