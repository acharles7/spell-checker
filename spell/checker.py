"""This module analyze the comments and docstrings"""

import re
from pathlib import Path

from textblob import Word  # type: ignore

from spell.types import Text

WORDS_ASSETS: Path = Path(__file__).parent.parent / "assets"

PY_STD_LIB_PATH: Path = WORDS_ASSETS / "std_lib_names"
TECH_WORDS_PATH: Path = WORDS_ASSETS / "tech_words"
COMMON_WORDS_PATH: Path = WORDS_ASSETS / "common"

EXTENSIONS: set[str] = {".py", ".txt", ".md"}
KNOWN_WORDS: set[str] = set()
IGNORE_WORDS: set[str] = {"fixme", "todo"}
PY_STD_LIB: set[str] = {w for w in PY_STD_LIB_PATH.read_text().split()}
TECH_WORDS: set[str] = {w for w in TECH_WORDS_PATH.read_text().split()}
COMMON_WORDS: set[str] = {w for w in COMMON_WORDS_PATH.read_text().split()}


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

    @property
    def ignorable(self) -> bool:
        """Return True if given word is known to spell-checker"""
        return self.word in PY_STD_LIB.union(TECH_WORDS).union(COMMON_WORDS)


class Checker:
    def __init__(self, text: Text):
        self.text: Text = text

    def check(self, verbose: bool = False) -> None:
        for word in self.text.split():

            _word = _Word(word.lower())

            if _word.is_known or _word.is_function or _word.is_extension or _word.ignorable:
                if verbose:
                    print(f"<<<< Skipping word: {_word}")
                continue

            spelling_check = _word.spellcheck()
            if verbose:
                print(f">>>> Including word: {_word}")
                print("->", spelling_check)

            spelling, confidence = spelling_check[0]
            if confidence == 1:
                if verbose:
                    print("Correct word", _word)
            else:
                print(f"Did you mean this '{spelling}' ?", _word)

        print("-" * 50)

    @property
    def lower(self) -> str:
        return self.text.lower()

    @property
    def split(self) -> list[str]:
        return self.text.split()
