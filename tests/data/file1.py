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
        # convert str to int
        if isinstance(self.v, str):
            return int(self.v)
        # convert to str & then int
        elif isinstance(self.v, list):
            return int("".join([str(v) for v in self.v]))
        # try to cast to int
        else:
            return int(self.v)
