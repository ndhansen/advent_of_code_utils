from pathlib import Path

import pytest

from aoc import puzzle


@pytest.mark.parametrize("test", [True, False])
def test_get_puzzle_input(tmp_path: Path, *, test: bool) -> None:
    test_input = "abc\n123"
    test_file_path = Path(tmp_path / "input.txt")
    with test_file_path.open("w") as test_file:
        test_file.write(test_input)

    puzzle_input = puzzle.get_puzzle_input(test_file_path, test=test)

    assert puzzle_input.test is test
    assert puzzle_input.raw == "abc\n123"
    assert puzzle_input.lines == ["abc", "123"]
