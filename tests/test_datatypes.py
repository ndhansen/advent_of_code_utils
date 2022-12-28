from aoc import Coord


def test_coord_get_neighbors() -> None:
    # Create a coord in any spot
    point = Coord(1, 1)

    # Get the neighbors
    neighbors = point.get_neighbors()

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 8
    assert Coord(0, 0) in neighbors
    assert Coord(0, 1) in neighbors
    assert Coord(0, 2) in neighbors
    assert Coord(1, 0) in neighbors
    assert Coord(1, 2) in neighbors
    assert Coord(2, 0) in neighbors
    assert Coord(2, 1) in neighbors
    assert Coord(2, 2) in neighbors


def test_coord_get_neighbors_limited__within_bounds() -> None:
    # Create a coord in any spot
    point = Coord(1, 1)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 8
    assert Coord(0, 0) in neighbors
    assert Coord(0, 1) in neighbors
    assert Coord(0, 2) in neighbors
    assert Coord(1, 0) in neighbors
    assert Coord(1, 2) in neighbors
    assert Coord(2, 0) in neighbors
    assert Coord(2, 1) in neighbors
    assert Coord(2, 2) in neighbors


def test_coord_get_neighbors_limited__top_left() -> None:
    # Create a coord in the top left
    point = Coord(0, 0)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 3
    assert Coord(0, 1) in neighbors
    assert Coord(1, 0) in neighbors
    assert Coord(1, 1) in neighbors


def test_coord_get_neighbors_limited__bottom_right() -> None:
    # Create a coord in the bottom right
    point = Coord(2, 2)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 3
    assert Coord(1, 1) in neighbors
    assert Coord(2, 1) in neighbors
    assert Coord(1, 2) in neighbors


def test_coord_get_neighbors_limited__top_right() -> None:
    # Create a coord in the top right
    point = Coord(0, 2)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 3
    assert Coord(0, 1) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(1, 2) in neighbors


def test_coord_get_neighbors_limited__bottom_left() -> None:
    # Create a coord in the bottom left
    point = Coord(2, 0)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 3
    assert Coord(1, 0) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(2, 1) in neighbors


def test_coord_get_neighbors_limited__top_row() -> None:
    # Create a coord in the top row
    point = Coord(0, 1)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 5
    assert Coord(0, 0) in neighbors
    assert Coord(0, 2) in neighbors
    assert Coord(1, 0) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(1, 2) in neighbors


def test_coord_get_neighbors_limited__right_column() -> None:
    # Create a coord in the right column
    point = Coord(1, 2)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 5
    assert Coord(0, 1) in neighbors
    assert Coord(0, 2) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(2, 1) in neighbors
    assert Coord(2, 2) in neighbors


def test_coord_get_neighbors_limited__bottom_row() -> None:
    # Create a coord in the bottom row
    point = Coord(2, 1)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 5
    assert Coord(1, 0) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(1, 2) in neighbors
    assert Coord(2, 0) in neighbors
    assert Coord(2, 2) in neighbors


def test_coord_get_neighbors_limited__left_column() -> None:
    # Create a coord in the left column
    point = Coord(1, 0)

    # Get the neighbors
    neighbors = point.get_neighbors_limited(Coord(2, 2))

    # Check that all eight neighboring fields surround the point
    assert len(neighbors) == 5
    assert Coord(0, 0) in neighbors
    assert Coord(0, 1) in neighbors
    assert Coord(1, 1) in neighbors
    assert Coord(2, 0) in neighbors
    assert Coord(2, 1) in neighbors
