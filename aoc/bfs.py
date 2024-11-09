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


_default_neighbor_func = SimpleMappingNeighborFunc()


class _SearchPath[S](NamedTuple):
    path: list[S]
    cost: int

    @property
    def current(self) -> S:
        return self.path[-1]


def breadth_first_search(
    *,
    start: S,
    goal: S,
    paths: Mapping[S, set[S]],
    next_func: Neighbors = _default_neighbor_func,
) -> tuple[list[S], int]:
    start_path = _SearchPath([start], 0)
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
                    current_path.cost + 1,
                ),
            )

    msg = "No paths found"
    raise UnsolveableError(msg)
