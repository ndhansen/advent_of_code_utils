from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from importlib.metadata import entry_points
from importlib.resources import files
from types import FrameType, ModuleType
from typing import Any

from rich.console import Console
from rich.pretty import pprint

from aoc.puzzle import PuzzleInput


def _get_puzzle_input(module: ModuleType, *, day: str, test: bool) -> PuzzleInput:
    input_files = files(module)
    filename = "test.txt" if test else "input.txt"
    contents = input_files.joinpath("inputs", day, filename).read_text()
    return PuzzleInput.from_contents(contents=contents, test=test)


type TraceFunction = Callable[[FrameType, str, Any], TraceFunction | None]


def trace_function(
    frame: FrameType,
    event: str,
    arg: Any,  # noqa: ARG001, ANN401
) -> Callable[[FrameType, str, Any], TraceFunction]:
    if event == "return" and frame.f_code.co_name in ("part_1", "part_2"):
        pprint(
            dict(frame.f_locals),
            max_string=80,
            max_length=10,
            max_depth=3,
        )
    return trace_function


def _run_puzzles(day: ModuleType, puzzle_input: PuzzleInput) -> None:
    console = Console()
    print("Part 1:")  # noqa: T201
    try:
        print(day.part_1(puzzle_input))  # noqa: T201
    except Exception:  # noqa: BLE001
        console.print_exception(show_locals=True)
    print("Part 2:")  # noqa: T201
    try:
        print(day.part_2(puzzle_input))  # noqa: T201
    except Exception:  # noqa: BLE001
        console.print_exception(show_locals=True)


def run_day() -> None:
    parser = argparse.ArgumentParser(prog="AOC", description="Advent of Code")
    parser.add_argument("day", help="The day to run.")
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Whether to use the test or real input.",
    )
    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="Watch for updates and print all output live",
    )

    args = parser.parse_args()

    compatible_modules = entry_points(group="aoc")
    if len(compatible_modules) != 1:
        msg = "Found more or less than one advent of code modules."
        raise ValueError(msg)
    module = compatible_modules["base"].load()

    if args.day not in module.__all__:
        msg = f"Did not find day in in {module}"
        raise ValueError(msg)

    puzzle_input = _get_puzzle_input(module, day=args.day, test=args.test)

    day = getattr(module, args.day)
    if args.watch:
        sys.settrace(trace_function)
        _run_puzzles(day, puzzle_input)
        sys.settrace(None)
    else:
        _run_puzzles(day, puzzle_input)
