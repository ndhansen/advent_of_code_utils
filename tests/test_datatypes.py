import pytest

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


def test_coord_neg_zero() -> None:
    # Create a point at the origin
    point = Coord(0, 0)

    # Check that the negative is still at the origin
    assert -point == Coord(0, 0)


def test_coord_neg_positive() -> None:
    # Create a point at a positive x and y coordinate
    point = Coord(3, 6)

    # Check that the negative is negative in both axes
    assert -point == Coord(-3, -6)


def test_coord_neg_negative() -> None:
    # Create a point at a negative x and y coordinate
    point = Coord(-3, -6)

    # Check that the negative is positive in both axes
    assert -point == Coord(3, 6)


def test_add_invalid_type() -> None:
    with pytest.raises(TypeError):
        _ = Coord(0, 0) + 2


def test_coord_add() -> None:
    assert Coord(1, 3) + Coord(3, 2) == Coord(4, 5)


def test_sub_invalid_type() -> None:
    with pytest.raises(TypeError):
        _ = Coord(0, 0) - 2


def test_coord_sub() -> None:
    assert Coord(5, 2) - Coord(2, 3) == Coord(3, -1)
