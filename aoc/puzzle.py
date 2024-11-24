from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PuzzleInput:
    raw: str
    lines: list[str]
    test: bool

    @classmethod
    def from_contents(cls, *, contents: str, test: bool) -> PuzzleInput:
        raw = contents
        lines = [line.strip() for line in contents.splitlines()]
        return cls(raw, lines, test)


def get_puzzle_input(filepath: str | Path, *, test: bool) -> PuzzleInput:
    with Path(filepath).open() as file:
        contents = file.read()
    return PuzzleInput.from_contents(contents=contents, test=test)
