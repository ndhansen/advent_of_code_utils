from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PuzzleInput:
    raw: str
    lines: list[str]
    test: bool


def get_puzzle_input(filepath: str | Path, *, test: bool) -> PuzzleInput:
    with Path(filepath).open() as file:
        raw = file.read()
    with Path(filepath).open() as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    return PuzzleInput(raw=raw, lines=lines, test=test)
