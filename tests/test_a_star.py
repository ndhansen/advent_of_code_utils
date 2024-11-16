from collections.abc import Iterator, Mapping
from dataclasses import dataclass

import pytest

from aoc.a_star import Cost, Heuristic, Neighbors, a_star
from aoc.datatypes import Coord
from aoc.exceptions import UnsolveableError


@dataclass
class Maze:
    start: Coord
    end: Coord
    floors: set[Coord]
    walls: set[Coord]
    raw: list[str]

    @staticmethod
    def path_tiles() -> set[str]:
        return {"v", "^", "<", ">"}


def parse_predicted_path(maze: Maze) -> list[Coord]:
    path_symbols = Maze.path_tiles() | {"T"}
    for col, row in [(-1, 0), (0, 1), (0, -1), (1, 0)]:
        current = maze.start - Coord(row=row, col=col)
        if (
            current.col >= 0
            and current.col < len(maze.raw[0])
            and current.row >= 0
            and current.row < len(maze.raw)
            and maze.raw[current.row][current.col] in path_symbols
        ):
            break
    else:
        msg = "No path next to start found."
        raise ValueError(msg)

    path = [maze.start, current]
    while current != maze.end:
        char = maze.raw[current.row][current.col]
        match char:
            case "v":
                current += Coord(1, 0)
            case "^":
                current += Coord(-1, 0)
            case ">":
                current += Coord(0, 1)
            case "<":
                current += Coord(0, -1)
            case _:
                msg = "Invalid path."
                raise ValueError(msg)
        path.append(current)

    return path


def parse_maze(maze: str) -> Maze:
    """Take in a string that represents a maze.

    The structure of the maze is as follows:
    - Dots represent empty space
    - x's represent walls
    - S represents the starting position
    - T represents the end
    - Directional arrows show the expected fasted path.

    S..
    vx.
    >T.

    Args:
        maze: A visual map of a maze.

    Returns:
        A maze object, and the fastest path from the start to the goal (inclusive).
    """
    floor_tiles = Maze.path_tiles() | {"."}
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
                case default:
                    if default not in floor_tiles:
                        msg = f"Found invalid caracter {default}"
                        raise ValueError(msg)

                    floors.add(Coord(row, col))

    if not start or not end:
        msg = "Maze needs a start and end"
        raise ValueError(msg)

    return Maze(start=start, end=end, floors=floors, walls=walls, raw=maze.split("\n"))


class MazeHeuristic(Heuristic[Coord]):
    def __call__(self, current: Coord, target: Coord) -> float:
        row_diff = abs((current - target).row)
        col_diff = abs((current - target).col)
        return float(row_diff + col_diff)


class MazeNeighbors(Neighbors[Coord]):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def __call__(self, current: Coord, paths: Mapping[Coord, Coord]) -> Iterator[Coord]:  # noqa: ARG002
        for potential_neighbor in [Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1)]:
            neighbor = current + potential_neighbor
            if neighbor in self.maze.floors:
                yield neighbor


class MazeCost(Cost[Coord]):
    def __call__(self, paths: Mapping[Coord, Coord], current: Coord, last: Coord) -> float:  # noqa: ARG002
        return 1


# fmt: off
@pytest.mark.parametrize(
    "maze",
    [
        pytest.param(
            (
                "S>T"
            ),
            id="direct",
        ),
        pytest.param(
            (
                "S..\n"
                "vx.\n"
                ">T."
            ),
            id="middle_wall",
        ),
        pytest.param(
            (
                "S>>>>v\n"
                "xxxxxv\n"
                "v<<<<<\n"
                "vxxxxx\n"
                ">>>>>T\n"
            ),
            id="snake",
        ),
        pytest.param(
            (
                "S.....\n"
                "vxxxx.\n"
                "vx>>Tx\n"
                "vx^xx.\n"
                "vx^<<<\n"
                "vxxxx^\n"
                ">>>>>^\n"
                ".xxxx.\n"
                "......\n"
            ),
            id="maze",
        ),
    ],
)
# fmt: on
def test_direct(maze: str) -> None:
    test_maze = parse_maze(maze)
    expected_path = parse_predicted_path(test_maze)

    actual_path, actual_cost = a_star(
        test_maze.start,
        test_maze.end,
        MazeHeuristic(),
        MazeCost(),
        MazeNeighbors(test_maze),
    )

    assert expected_path == actual_path
    expected_cost = float(len(expected_path) - 1)
    assert expected_cost == actual_cost


def test_unsolveable() -> None:
    # fmt: off
    maze = (
        "Sx.\n"
        "xx.\n"
        "T..\n"
    )
    # fmt: on

    test_maze = parse_maze(maze)
    with pytest.raises(UnsolveableError):
        a_star(
            test_maze.start,
            test_maze.end,
            MazeHeuristic(),
            MazeCost(),
            MazeNeighbors(test_maze),
        )
