import heapq
from collections import defaultdict
from collections.abc import Iterator, Mapping
from typing import Protocol

from aoc.exceptions import UnsolveableError


class Heuristic[T](Protocol):
    def __call__(self, current: T, goal: T) -> float: ...


class Cost[T](Protocol):
    def __call__(self, paths: Mapping[T, T], current: T, last: T) -> float: ...


class Neighbors[T](Protocol):
    def __call__(self, current: T, paths: Mapping[T, T]) -> Iterator[T]: ...


def _reconstruct_path[T](paths: Mapping[T, T], start: T, goal: T) -> list[T]:
    path = [goal]
    current = goal
    while current in paths:
        path.insert(0, paths[current])
        current = paths[current]
        if current == start:
            break
    return path


def a_star[T](
    start: T,
    goal: T,
    heuristic: Heuristic[T],
    cost_func: Cost[T],
    next_func: Neighbors[T],
) -> tuple[list[T], float]:
    frontier: list[tuple[float, T]] = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    paths: dict[T, T] = {}
    cheapest_path: dict[T, float] = defaultdict(lambda: float("inf"))
    cheapest_path[start] = 0.0

    while len(frontier) > 0:
        _, current = heapq.heappop(frontier)
        if current == goal:
            path = _reconstruct_path(paths, start, goal)
            return path, cheapest_path[current]

        for neighbor in next_func(current, paths):
            new_cost = cheapest_path[current] + cost_func(paths, neighbor, current)

            if new_cost < cheapest_path[neighbor]:
                paths[neighbor] = current
                cheapest_path[neighbor] = new_cost
                heapq.heappush(
                    frontier,
                    (new_cost + heuristic(neighbor, goal), neighbor),
                )

    msg = "Could not find a path."
    raise UnsolveableError(msg)
