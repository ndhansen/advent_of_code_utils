from __future__ import annotations

import itertools
from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


class Coord(NamedTuple):
    row: int
    col: int

    def __add__(self, other: object) -> Coord:
        if isinstance(other, Coord):
            delta = other
        elif isinstance(other, Direction):
            match other:
                case Direction.NORTH:
                    delta = Coord(-1, 0)
                case Direction.SOUTH:
                    delta = Coord(1, 0)
                case Direction.WEST:
                    delta = Coord(0, -1)
                case Direction.EAST:
                    delta = Coord(0, 1)
        else:
            msg = "Coords can only be added with themselves and Directions."
            raise TypeError(msg)
        return Coord(self.row + delta.row, self.col + delta.col)

    def __neg__(self) -> Coord:
        return Coord(-self.row, -self.col)

    def __sub__(self, other: object) -> Coord:
        if not isinstance(other, Coord):
            msg = "Only Coords can be subtracted."
            raise TypeError(msg)
        return Coord(self.row - other.row, self.col - other.col)

    def get_neighbors(self) -> list[Coord]:
        """Get all neighboring coords to coordinate.

        Returns:
            All coordinates neighboring this coordinate.
        """
        all_neighbors = []
        for row, col in itertools.product(range(-1, 2, 1), repeat=2):
            if row == 0 and col == 0:
                continue
            all_neighbors.append(Coord(self.row + row, self.col + col))
        return all_neighbors

    def get_neighbors_limited(self, corner: Coord) -> list[Coord]:
        """Gets all neighboring coords to the coordinate, but stays within the bounds of given by
        the corner.

        Args:
            corner: The corner of the area, which represents the largest possible row and column.

        Returns:
            All the coordinates surrounding the current coordinate, that do not exceed the bounds
            of the corner.
        """
        neighbors = self.get_neighbors()

        def filter_below_bounds(coord: Coord) -> bool:
            return coord.row > -1 and coord.col > -1

        # Filter out neighbors that are smaller than the top row or left column
        neighbors = list(filter(filter_below_bounds, neighbors))

        def filter_above_bounds(coord: Coord) -> bool:
            return coord.row <= corner.row and coord.col <= corner.col

        # Filter out the neighbors that are larger than the corner row or column
        return list(filter(filter_above_bounds, neighbors))
