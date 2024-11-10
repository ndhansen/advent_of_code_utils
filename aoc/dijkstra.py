from __future__ import annotations

import heapq
from collections.abc import Hashable, Iterator, Mapping
from typing import Any, NamedTuple, Protocol

from aoc.exceptions import UnsolveableError


class Neighbors[S: Hashable](Protocol):
    def __call__(self, current: S, paths: Mapping[S, set[S]]) -> Iterator[S]: ...


class SimpleMappingNeighborFunc[S: Hashable](Neighbors[S]):
    def __call__(self, current: S, paths: Mapping[S, set[S]]) -> Iterator[S]:
        if current not in paths:
            return
        yield from paths[current]


class Cost[S: Hashable](Protocol):
    def __call__(self, paths: Mapping[S, set[S]], current: S, last: S) -> float: ...


_default_neighbor_func = SimpleMappingNeighborFunc[Any]()


class _SearchPath[S: Hashable](NamedTuple):
    path: list[S]
    cost: float

    @property
    def current(self) -> S:
        return self.path[-1]


def dijkstra[S: Hashable](
    *,
    start: S,
    goal: S,
    paths: Mapping[S, set[S]],
    cost_func: Cost[S],
    next_func: Neighbors[S] = _default_neighbor_func,
) -> tuple[list[S], float]:
    start_path = _SearchPath([start], 0.0)
    frontier = [(start_path.cost, start_path)]
    seen = set()
    while frontier:
        _, current_path = heapq.heappop(frontier)
        if current_path.current == goal:
            return current_path.path, current_path.cost
        if current_path.current in seen:
            continue
        seen.add(current_path.current)

        for next_node in next_func(current_path.current, paths=paths):
            next_search_path = _SearchPath(
                [*current_path.path, next_node],
                current_path.cost + cost_func(paths, next_node, current_path.current),
            )
            heapq.heappush(frontier, (next_search_path.cost, next_search_path))

    msg = "No paths found"
    raise UnsolveableError(msg)
