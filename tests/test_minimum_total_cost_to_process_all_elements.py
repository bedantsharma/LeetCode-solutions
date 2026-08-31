"""Tests for Solutions/MinimumTotalCostToProcessAllElements.py
(LeetCode 3987. Minimum Total Cost to Process All Elements).

Problem (from https://leetcode.com/problems/minimum-total-cost-to-process-all-elements/):
    You start with `k` units of resources and must process `nums` left to
    right. Processing nums[i] consumes nums[i] resources. Whenever the
    available resources are less than nums[i], you may perform an
    operation that adds k resources; the 1st such operation costs 1, the
    2nd costs 2, etc. (Multiple operations can be needed for a single
    element if the shortfall exceeds k.) Return the minimum total cost
    (mod 1e9+7) needed to process every element.

Two layers of coverage:

1. Official/fixed examples - the three worked examples from the LeetCode
   problem statement, plus a couple of hand-picked boundary cases
   (including one that needs several catch-up operations for a single
   element).

2. Randomized property-based testing - `reference_min_cost` is a naive,
   obviously-correct oracle (plain `while` simulation) that shares no
   code with the solution under test. Many random (nums, k) inputs are
   checked against it.

See ../CLAUDE.md: this file only tests
Solutions/MinimumTotalCostToProcessAllElements.py, it never modifies it.
"""

from __future__ import annotations

import os
import random

import pytest

from Solutions.MinimumTotalCostToProcessAllElements import Solution

MOD = 10 ** 9 + 7


# ---------------------------------------------------------------------------
# Reference oracle - deliberately naive/obviously-correct, independent of
# the solution's internal logic.
# ---------------------------------------------------------------------------

def reference_min_cost(nums: list[int], k: int) -> int:
    cur = k
    ops = 0
    for x in nums:
        while cur < x:
            cur += k
            ops += 1
        cur -= x
    return (ops * (ops + 1) // 2) % MOD


# ---------------------------------------------------------------------------
# Official LeetCode examples
# ---------------------------------------------------------------------------

OFFICIAL_EXAMPLES = [
    pytest.param([1, 2, 3, 4], 4, 3, id="example-1-two-single-ops"),
    pytest.param([1, 1, 7, 14], 4, 15, id="example-2-needs-multi-op-catchup"),
    pytest.param([1, 2, 3, 4], 10, 0, id="example-3-never-runs-short"),
]


@pytest.mark.parametrize("nums,k,expected", OFFICIAL_EXAMPLES)
def test_official_examples(nums, k, expected):
    assert Solution().minimumCost(nums[:], k) == expected


# ---------------------------------------------------------------------------
# Fixed edge cases
# ---------------------------------------------------------------------------

EDGE_CASES = [
    pytest.param([5], 5, 0, id="single-element-exactly-enough"),
    pytest.param([6], 5, 1, id="single-element-needs-one-op"),
    pytest.param([1, 1, 1, 1], 1000, 0, id="huge-k-never-tops-up"),
    pytest.param([1], 1, 0, id="minimal-input-no-op-needed"),
    # 100 needs 99 catch-up ops of size 1 -> triangular(99) = 99*100/2
    pytest.param([100], 1, 4950, id="single-huge-deficit-needs-many-ops"),
    # first element already exceeds k by more than k -> multiple ops
    # before any element is even fully consumed.
    pytest.param([25, 1, 1], 10, 3, id="first-element-needs-two-ops"),
]


@pytest.mark.parametrize("nums,k,expected", EDGE_CASES)
def test_edge_cases(nums, k, expected):
    assert Solution().minimumCost(nums[:], k) == expected


def test_no_operations_ever_needed_returns_zero():
    # Every element is fully covered by the initial k resources.
    nums = [1, 1, 1, 1, 1]
    assert Solution().minimumCost(nums, 5) == 0


def test_does_not_mutate_input_list():
    nums = [1, 2, 3, 4]
    Solution().minimumCost(nums, 4)
    assert nums == [1, 2, 3, 4]


# ---------------------------------------------------------------------------
# Randomized property-based testing
# ---------------------------------------------------------------------------

TRIALS = 300
MAX_LEN = 60
MAX_NUM = 300
MAX_K = 50


def generate_case(rng: random.Random) -> tuple[list[int], int]:
    length = rng.randint(1, MAX_LEN)
    k = rng.randint(1, MAX_K)
    nums = [rng.randint(1, MAX_NUM) for _ in range(length)]
    return nums, k


def _make_rng() -> tuple[random.Random, int]:
    """A fresh seed each run, but overridable/reproducible via env var."""
    seed = int(os.environ.get("MINCOST_SEED", random.SystemRandom().randrange(2 ** 32)))
    return random.Random(seed), seed


def test_randomized_against_reference():
    rng, seed = _make_rng()
    solution = Solution()

    for trial in range(TRIALS):
        nums, k = generate_case(rng)

        expected = reference_min_cost(nums, k)
        actual = solution.minimumCost(nums[:], k)

        assert actual == expected, (
            f"Mismatch on trial {trial} with MINCOST_SEED={seed}\n"
            f"nums={nums}\nk={k}\nexpected={expected}, got={actual}"
        )


def test_randomized_result_is_a_nonnegative_int_below_mod():
    """Sanity property: the return value is always a non-negative int,
    reduced mod 1e9+7."""
    rng, seed = _make_rng()
    solution = Solution()

    for trial in range(TRIALS):
        nums, k = generate_case(rng)

        result = solution.minimumCost(nums[:], k)

        assert isinstance(result, int), (
            f"Trial {trial} MINCOST_SEED={seed}: expected int, got {type(result)}"
        )
        assert 0 <= result < MOD, (
            f"Trial {trial} MINCOST_SEED={seed}: result {result} out of [0, mod) range"
        )
