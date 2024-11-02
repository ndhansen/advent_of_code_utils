from collections.abc import Iterator
from dataclasses import dataclass

from aoc.datatypes import Coord
from aoc.search import Cost, Heuristic, Neighbors, a_star


@dataclass
class Maze:
    start: Coord
    end: Coord
    floors: set[Coord]
    walls: set[Coord]


def parse_maze(maze: str) -> Maze:
    """Take in a string that represents a maze.

    The structure of the maze are dots for empty space, and x for walls, S for
    start, and T for target.

    S..
    .x.
    ..T

    Args:
        maze: A visual map of a maze.

    Returns:
        A maze object with start, end, and sets of floors and walls.
    """
    start = None
    end = None
    floors: set[Coord] = set()
    walls: set[Coord] = set()
    for row, line in enumerate(maze.split("\n")):
        for col, char in enumerate(list(line)):
            match char:
                case "S":
                    start = Coord(row, col)
                    floors.add(Coord(row, col))
                case "T":
                    end = Coord(row, col)
                    floors.add(Coord(row, col))
                case "x":
                    walls.add(Coord(row, col))
                case ".":
                    floors.add(Coord(row, col))

    if not start or not end:
        msg = "Maze needs a start and end"
        raise ValueError(msg)

    return Maze(start=start, end=end, floors=floors, walls=walls)


class MazeHeuristic(Heuristic):
    def __call__(self, current: Coord, target: Coord) -> float:
        row_diff = abs((current - target).row)
        col_diff = abs((current - target).col)
        return float(row_diff + col_diff)


class MazeNeighbors(Neighbors):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def __call__(self, current: Coord, paths: dict[Coord, Coord]) -> Iterator[Coord]:  # noqa: ARG002
        for potential_neighbor in [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]:
            neighbor = current + potential_neighbor
            if neighbor in self.maze.floors:
                yield neighbor


class MazeCost(Cost):
    def __call__(self, paths: dict[Coord, Coord], current: Coord, last: Coord) -> float:  # noqa: ARG002
        return 1


def test_direct() -> None:
    test_maze = parse_maze("S.T")
    expected_path = [Coord(0, 0), Coord(0, 1), Coord(0, 2)]
    expected_cost = 2

    actual_path, actual_cost = a_star(
        test_maze.start,
        test_maze.end,
        MazeHeuristic(),
        MazeCost(),
        MazeNeighbors(test_maze),
    )

    assert expected_path == actual_path
    assert expected_cost == actual_cost


def test_middle_wall() -> None:
    # fmt: off
    maze = (
        "S..\n"
        ".x.\n"
        ".T."
    )
    # fmt: on

    test_maze = parse_maze(maze)
    expected_path = [Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(2, 1)]
    expected_cost = 3

    actual_path, actual_cost = a_star(
        test_maze.start,
        test_maze.end,
        MazeHeuristic(),
        MazeCost(),
        MazeNeighbors(test_maze),
    )

    assert expected_path == actual_path
    assert expected_cost == actual_cost
