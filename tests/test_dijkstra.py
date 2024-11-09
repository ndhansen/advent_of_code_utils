from collections.abc import Mapping

import pytest

from aoc import dijkstra
from aoc.exceptions import UnsolveableError


class CostMappingFunc[S](dijkstra.Cost):
    def __init__(self, cost_map: Mapping[tuple[S, S], float]) -> None:
        self.cost_map = cost_map

    def __call__(self, paths: Mapping[S, set[S]], current: S, last: S) -> float:  # noqa: ARG002
        return self.cost_map[(last, current)]


def test_dijkstra__faster_path() -> None:
    paths = {
        "A": {"B", "C"},
        "B": {"C"},
    }
    cost_map = {
        ("A", "B"): 1,
        ("B", "C"): 1,
        ("A", "C"): 3,
    }

    cost_func = CostMappingFunc(cost_map=cost_map)
    path, cost = dijkstra.dijkstra(start="A", goal="C", paths=paths, cost_func=cost_func)
    assert path == ["A", "B", "C"]
    assert cost == 2.0


def test_dijkstra__no_solution() -> None:
    paths = {
        "A": {"B", "E"},
        "C": {"D"},
        "E": {"A", "B"},
    }

    cost_func = lambda _, __, ___: 1
    with pytest.raises(UnsolveableError):
        dijkstra.dijkstra(start="A", goal="D", paths=paths, cost_func=cost_func)
