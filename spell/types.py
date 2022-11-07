import string
from dataclasses import dataclass
from enum import Enum
from typing import NewType, Protocol

Comment = NewType("Comment", str)
Docstring = NewType("Docstring", str)


@dataclass
class Text(str):

    text: str

    def remove_symbols(self) -> "Text":
        """Remove punctuations from the given text"""
        s = self.text
        for char in string.punctuation:
            s = s.replace(char, " ")
        return Text(s)


class Ignore(Enum):

    TODO = "TODO"

    FIXME = "FIXME"


class Type(Enum):
    """Type of comments in a python file"""

    #: Inline comments starts with '#'
    INLINE = "INLINE"

    #: Docstring of module, class, or function
    DOCSTRING = "DOCSTRING"


class CommentType(Enum):

    INLINE = "inline"

    CLASS = "class"

    MODULE = "module"

    FUNCTION = "function"


class Processor(Protocol):
    """A Processor class to process the text"""

    def clean(self) -> None:
        """Returns a clean version of text"""
        ...

    def text(self) -> str:
        """Return plain text of docstring and comments"""
        ...

    def remove_symbols(self) -> str:
        """Remove symbols/punctuations from text"""
        ...

    def has_code(self) -> bool:
        """Returns bool if text contains any code snippet/line"""
        ...
