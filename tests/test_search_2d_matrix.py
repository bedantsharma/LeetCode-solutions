"""Tests for Solutions/Search2DMatrix.py (LeetCode 74. Search a 2D Matrix).

Two layers of coverage:

1. Fixed edge cases - small, hand-picked matrices that exercise the
   boundaries of the problem (single row/column, negative numbers,
   duplicates within a row, values that sit just outside the matrix, etc).

2. Randomized property-based testing - `generate_valid_matrix` builds
   random matrices that honestly satisfy the two problem invariants:
     * each row is sorted in non-decreasing order
     * the first value of each row is strictly greater than the last
       value of the previous row
   A trivial linear-scan oracle (`brute_force_search`) is used as the
   ground truth, since it is obviously correct and doesn't share any
   logic with the binary-search solution under test. Many random
   (matrix, target) pairs are generated per run and checked against the
   oracle.

See ../CLAUDE.md: this file only tests Solutions/Search2DMatrix.py, it
never modifies it.
"""

from __future__ import annotations

import os
import random

import pytest

from Solutions.Search2DMatrix import Solution


# ---------------------------------------------------------------------------
# Fixed edge cases
# ---------------------------------------------------------------------------

EDGE_CASES = [
    # (matrix, target, expected, id)
    pytest.param([[1]], 1, True, id="1x1-hit"),
    pytest.param([[1]], 2, False, id="1x1-miss"),
    pytest.param([[1, 3, 5, 7]], 5, True, id="single-row-hit"),
    pytest.param([[1, 3, 5, 7]], 6, False, id="single-row-miss"),
    pytest.param([[1], [3], [5], [7]], 5, True, id="single-column-hit"),
    pytest.param([[1], [3], [5], [7]], 4, False, id="single-column-miss"),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        3,
        True,
        id="leetcode-example-1",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        13,
        False,
        id="leetcode-example-2",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        1,
        True,
        id="matrix-first-element",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        60,
        True,
        id="matrix-last-element",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        7,
        True,
        id="last-element-of-a-row",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        10,
        True,
        id="first-element-of-a-row",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        8,
        False,
        id="gap-between-rows",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        0,
        False,
        id="below-min",
    ),
    pytest.param(
        [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]],
        61,
        False,
        id="above-max",
    ),
    pytest.param(
        [[-10, -5, -5, 0], [3, 3, 3, 8]],
        -5,
        True,
        id="negative-numbers-and-duplicates",
    ),
    pytest.param(
        [[-10, -5, -5, 0], [3, 3, 3, 8]],
        3,
        True,
        id="duplicate-run-within-row",
    ),
    pytest.param(
        [[-10, -5, -5, 0], [3, 3, 3, 8]],
        1,
        False,
        id="miss-inside-duplicate-gap",
    ),
]


@pytest.mark.parametrize("matrix,target,expected", EDGE_CASES)
def test_edge_cases(matrix, target, expected):
    result = Solution().searchMatrix([row[:] for row in matrix], target)
    assert result == expected, f"matrix={matrix}, target={target}"


# ---------------------------------------------------------------------------
# Randomized property-based testing
# ---------------------------------------------------------------------------

TRIALS = 300
MAX_ROWS = 12
MAX_COLS = 12


def generate_valid_matrix(rng: random.Random) -> list[list[int]]:
    """Build a random matrix that satisfies the problem's invariants:

    - each row is sorted in non-decreasing order
    - the first value of a row is strictly greater than the last value
      of the previous row
    """
    m = rng.randint(1, MAX_ROWS)
    n = rng.randint(1, MAX_COLS)

    value = rng.randint(-50, 50)
    flat: list[int] = []
    for i in range(m * n):
        starts_new_row = i % n == 0
        if i != 0 and starts_new_row:
            value += rng.randint(1, 5)  # strict jump between rows
        elif i != 0:
            value += rng.randint(0, 3)  # non-decreasing within a row
        flat.append(value)

    return [flat[r * n:(r + 1) * n] for r in range(m)]


def brute_force_search(matrix: list[list[int]], target: int) -> bool:
    """Ground-truth oracle: plain linear scan, no binary search involved."""
    return any(target == value for row in matrix for value in row)


def _make_rng() -> tuple[random.Random, int]:
    """A fresh seed each run, but overridable/reproducible via env var."""
    seed = int(os.environ.get("SEARCH2D_SEED", random.SystemRandom().randrange(2**32)))
    return random.Random(seed), seed


def test_randomized_against_brute_force():
    rng, seed = _make_rng()
    solution = Solution()

    for trial in range(TRIALS):
        matrix = generate_valid_matrix(rng)
        flat = [value for row in matrix for value in row]

        if rng.random() < 0.5:
            # Guaranteed hit: sample an existing value.
            target = rng.choice(flat)
        else:
            # Usually a miss, occasionally a hit - both are valid signal.
            target = rng.randint(min(flat) - 10, max(flat) + 10)

        expected = brute_force_search(matrix, target)
        actual = solution.searchMatrix([row[:] for row in matrix], target)

        assert actual == expected, (
            f"Mismatch on trial {trial} with SEARCH2D_SEED={seed}\n"
            f"matrix={matrix}\ntarget={target}\n"
            f"expected={expected}, got={actual}"
        )


def test_randomized_all_hits():
    """Dedicated pass that only ever searches for values known to be present."""
    rng, seed = _make_rng()
    solution = Solution()

    for trial in range(TRIALS):
        matrix = generate_valid_matrix(rng)
        flat = [value for row in matrix for value in row]
        target = rng.choice(flat)

        actual = solution.searchMatrix([row[:] for row in matrix], target)

        assert actual is True, (
            f"Expected hit on trial {trial} with SEARCH2D_SEED={seed}\n"
            f"matrix={matrix}\ntarget={target}, got={actual}"
        )
