from collections import deque
from collections.abc import Iterator, Mapping
from typing import NamedTuple, Protocol, TypeVar

from aoc.exceptions import UnsolveableError

S = TypeVar("S")


class Neighbors(Protocol):
    def __call__(self, current: S, paths: Mapping[S, set[S]]) -> Iterator[S]: ...


class SimpleMappingNeighborFunc(Neighbors):
    def __call__(self, current: S, paths: Mapping[S, set[S]]) -> Iterator[S]:
        if current not in paths:
            return
        yield from paths[current]


class Cost(Protocol):
    def __call__(self, paths: Mapping[S, set[S]], current: S, last: S) -> float: ...


_default_neighbor_func = SimpleMappingNeighborFunc()


class _SearchPath[S](NamedTuple):
    path: list[S]
    cost: float

    @property
    def current(self) -> S:
        return self.path[-1]


def dijkstra(
    *,
    start: S,
    goal: S,
    paths: Mapping[S, set[S]],
    cost_func: Cost,
    next_func: Neighbors = _default_neighbor_func,
) -> tuple[list[S], float]:
    start_path = _SearchPath([start], 0.0)
    frontier = deque([start_path])
    seen = set()
    while frontier:
        current_path = frontier.popleft()
        if current_path.current == goal:
            return current_path.path, current_path.cost
        if current_path.current in seen:
            continue
        seen.add(current_path.current)

        for next_node in next_func(current_path.current, paths=paths):
            frontier.append(
                _SearchPath(
                    [*current_path.path, next_node],
                    current_path.cost + cost_func(paths, next_node, current_path.current),
                ),
            )

    msg = "No paths found"
    raise UnsolveableError(msg)
