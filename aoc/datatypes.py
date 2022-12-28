import itertools
from typing import NamedTuple


class Coord(NamedTuple):
    row: int
    col: int

    def get_neighbors(self) -> list["Coord"]:
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

    def get_neighbors_limited(self, corner: "Coord") -> list["Coord"]:
        """Gets all neighboring coords to the coordinate, but stays within the bounds of given by
        the corner.

        Args:
            corner: The corner of the area, which represents the largest possible row and column.

        Returns:
            All the coordinates surrounding the current coordinate, that do not exceed the bounds
            of the corner.
        """
        neighbors = self.get_neighbors()
        # Filter out neighbors that are smaller than the top row or left column
        neighbors = list(filter(lambda coord: coord.row > -1 and coord.col > -1, neighbors))
        # Filter out the neighbors that are larger than the corner row or column
        neighbors = list(
            filter(lambda coord: coord.row <= corner.row and coord.col <= corner.col, neighbors)
        )
        return neighbors
