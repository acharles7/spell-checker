from pathlib import Path
from spell.parser import FileParser, BaseComment


def test_inline_comments():
    file = Path.cwd() / "data" / "file1.py"
    parser = FileParser(file)
    parser.parse()

    actual_comments = parser.find_inline_comments()
    expected_comments = [
        BaseComment(comment='        # If string integer, then convert to integer', line_no=16),
        BaseComment(comment='        # if list, then convert it to string and then integer', line_no=19),
        BaseComment(comment='        # if no str, list, then debug the input', line_no=22),
    ]
    for a, b in zip(actual_comments, expected_comments):
        assert a.comment == b.comment

    expected_comments_cleaned = [
        BaseComment(comment='# If string integer, then convert to integer', line_no=16),
        BaseComment(comment='# if list, then convert it to string and then integer', line_no=19),
        BaseComment(comment='# if no str, list, then debug the input', line_no=22),
    ]
    for a, b in zip(actual_comments, expected_comments_cleaned):
        assert a.clean() == b

    expected_comments_stripped = [
        BaseComment(comment='If string integer, then convert to integer', line_no=16),
        BaseComment(comment='if list, then convert it to string and then integer', line_no=19),
        BaseComment(comment='if no str, list, then debug the input', line_no=22),
    ]
    for a, b in zip(actual_comments, expected_comments_stripped):
        assert a.clean(strip_hash=True) == b
