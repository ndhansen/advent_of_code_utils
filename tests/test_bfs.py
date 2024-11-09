import pytest

from aoc import bfs
from aoc.exceptions import UnsolveableError


def test_bfs__defaults() -> None:
    paths = {
        "A": {"B", "C"},
        "C": {"D"},
    }

    path, cost = bfs.breadth_first_search(start="A", goal="D", paths=paths)
    assert path == ["A", "C", "D"]
    assert cost == 2.0


def test_bfs__no_solution() -> None:
    paths = {
        "A": {"B", "E"},
        "C": {"D"},
        "E": {"A", "B"},
    }

    with pytest.raises(UnsolveableError):
        bfs.breadth_first_search(start="A", goal="D", paths=paths)
