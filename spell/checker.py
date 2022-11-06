"""This module analyze the comments and docstrings"""

import re

from textblob import Word  # type: ignore

from spell.types import Text

EXTENSIONS: set[str] = {".py", ".txt", ".md"}
KNOWN_WORDS: set[str] = set()
IGNORE_WORDS: set[str] = {"fixme", "todo"}


def remove_symbols(words: list[str]) -> list[str]:
    w = [re.sub(r"[^A-Za-z0-9]+", "", word) for word in words]
    return w


class _Word(Word):
    def __init__(self, word: str):
        self.word = word
        super().__init__(self.word)

    @property
    def is_function(self) -> bool:
        """Return True if given word is function"""
        return "()" in self.word

    @property
    def is_extension(self) -> bool:
        """Return True if given word is some kind of extension (e.g. .py, .txt. .doc)"""
        return self.word in EXTENSIONS

    @property
    def is_known(self) -> bool:
        """Return True if given word is known to spell-checker"""
        return self.word in KNOWN_WORDS


class Checker:
    def __init__(self, text: Text):
        self.text: Text = text

    def check(self) -> None:
        for word in self.text.split():

            _word = _Word(word.lower())

            if _word.is_known or _word.is_function or _word.is_extension:
                print(f"<<<< Skipping word: {_word}")
                continue
            print(f">>>> Including word: {_word}")
            print(f"spell check: {_word.spellcheck()}")
            print(f"check function: {_word.is_function}")
            print(f"check ext: {_word.is_extension}")
        print("-" * 50)

    @property
    def lower(self) -> str:
        return self.text.lower()

    @property
    def split(self) -> list[str]:
        return self.text.split()
