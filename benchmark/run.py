from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
import timeit

import pytomlpp
import qtoml

# import rtoml
import toml
import tomli
import tomlkit

import tomli_w

test_data_file = Path(__file__).parent / "data.toml"
test_data = tomli.loads(test_data_file.read_bytes().decode())
# Make the game fair for tomlkit by converting `test_data` to a
# tomlkit native type before measurements.
tomlkit_test_data = tomlkit.item(test_data)


def benchmark(
    name: str,
    run_count: int,
    func: Callable,
    col_width: tuple,
    compare_to: float | None = None,
) -> float:
    placeholder = "Running..."
    print(f"{name:>{col_width[0]}} | {placeholder}", end="", flush=True)
    time_taken = timeit.timeit(func, number=run_count)
    print("\b" * len(placeholder), end="")
    time_suffix = " s"
    print(f"{time_taken:{col_width[1]-len(time_suffix)}.3g}{time_suffix}", end="")
    if compare_to is None:
        print(" | baseline (100%)", end="")
    else:
        delta = compare_to / time_taken
        print(f" | {delta:.2%}", end="")
    print()
    return time_taken


def run(run_count: int) -> None:
    col_width = (10, 10, 28)
    col_head = ("parser", "exec time", "performance (more is better)")
    print(f"Dumping test data to a string {run_count} times:")
    print("-" * col_width[0] + "---" + "-" * col_width[1] + "---" + col_width[2] * "-")
    print(
        f"{col_head[0]:>{col_width[0]}} | {col_head[1]:>{col_width[1]}} | {col_head[2]}"
    )
    print("-" * col_width[0] + "-+-" + "-" * col_width[1] + "-+-" + col_width[2] * "-")
    # fmt: off
    baseline = benchmark("pytomlpp", run_count, lambda: pytomlpp.dumps(test_data), col_width)  # noqa: E501
    # benchmark("rtoml", run_count, lambda: rtoml.dumps(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("tomli", run_count, lambda: tomli_w.dumps(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("toml", run_count, lambda: toml.dumps(test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("tomlkit", run_count, lambda: tomlkit.dumps(tomlkit_test_data), col_width, compare_to=baseline)  # noqa: E501
    benchmark("qtoml", run_count, lambda: qtoml.dumps(test_data), col_width, compare_to=baseline)  # noqa: E501
    # fmt: on


if __name__ == "__main__":
    run(5000)
