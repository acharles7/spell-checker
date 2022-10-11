"""A python test file"""
from typing import Any


def hello() -> str:
    """Returns 'hello'"""
    return "hello"


class Converter:
    """A class represents foo and bar"""

    def __init__(self, value: Any = "10101"):
        self.v = value

    def convert(self) -> int:
        """Converts to integer representation"""
        # If string integer, then convert to integer
        if isinstance(self.v, str):
            return int(self.v)
        # if list, then convert it to string and then integer
        elif isinstance(self.v, list):
            return int("".join([str(v) for v in self.v]))
        # if no str, list, then try to cast it to int
        else:
            return int(self.v)
