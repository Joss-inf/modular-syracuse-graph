#!/usr/bin/env python3
"""
Verification script for modular Syracuse graph G_p.
Numerical checks for small values of p (p=2,3,4,5).
"""

import numpy as np
from collections import deque
from itertools import product


# ----------------------------------------------------------------------
# 1. GRAPH CONSTRUCTION
# ----------------------------------------------------------------------
def build_syracuse_graph(p: int) -> tuple[dict[int, list[int]], int]:
    """
    Build the modular Syracuse graph G_p on Z/2^pZ.

    Args:
        p: exponent (>= 2)

    Returns:
        adj: dict mapping vertex -> list of successors
        n: number of vertices (2^p)
    """
    n = 2 ** p
    adj = {i: [] for i in range(n)}

    for x in range(n):
        if x % 2 == 0:
            # Even: two successors
            half = x // 2
            adj[x] = [half, (half + n // 2) % n]
        else:
            # Odd: unique successor
            adj[x] = [(3 * x + 1) % n]

    return adj, n


def adjacency_matrix(adj: dict[int, list[int]], n: int) -> np.ndarray:
    """Convert adjacency dict to a dense (n x n) integer matrix."""
    A = np.zeros((n, n), dtype=int)
    for u in range(n):
        for v in adj[u]:
            A[u, v] += 1
    return A


# ----------------------------------------------------------------------
# 2. ALL-PAIRS SHORTEST PATHS (Floyd-Warshall)
# ----------------------------------------------------------------------
def floyd_warshall(adj: dict[int, list[int]], n: int) -> list[list[float]]:
    """
    Compute all-pairs shortest path distances.

    Returns:
        dist: n x n matrix where dist[i][j] is the shortest path length.
    """
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]

    for u in range(n):
        dist[u][u] = 0
        for v in adj[u]:
            dist[u][v] = 1

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# ----------------------------------------------------------------------
# 3. DIAMETER VERIFICATION
# ----------------------------------------------------------------------
def verify_diameter(p: int, expected: int) -> tuple[int, tuple[int, int]]:
    """
    Verify that diam(G_p) == expected.

    Returns:
        (diameter, (worst_start, worst_end))
    """
    adj, n = build_syracuse_graph(p)
    dist = floyd_warshall(adj, n)

    max_dist = 0
    worst_pair = (0, 0)

    for i in range(n):
        for j in range(n):
            if dist[i][j] == float('inf'):
                raise ValueError(f"Graph not strongly connected for p={p}!")
            if dist[i][j] > max_dist:
                max_dist = dist[i][j]
                worst_pair = (i, j)

    assert max_dist == expected, \
        f"FAILED: diam(G_{p}) = {max_dist}, expected {expected}"

    print(f"  ✓ diam(G_{p}) = {max_dist} (expected {expected})")
    print(f"    Worst pair: {worst_pair}")
    return max_dist, worst_pair


# ----------------------------------------------------------------------
# 4. PRIMITIVITY EXPONENT VERIFICATION
# ----------------------------------------------------------------------
def matrix_power_positive(A: np.ndarray, k: int) -> bool:
    """Return True iff all entries of A^k are strictly positive."""
    Ak = np.linalg.matrix_power(A, k)
    return np.all(Ak > 0)


def verify_primitivity(p: int, expected: int) -> int:
    """
    Verify that exp(G_p) == expected.
    Checks that A^(expected-1) has zeros and A^expected is all positive.
    """
    adj, n = build_syracuse_graph(p)
    A = adjacency_matrix(adj, n)

    # Check (expected-1) is NOT fully positive
    if expected > 1:
        is_pos_minus1 = matrix_power_positive(A, expected - 1)
        assert not is_pos_minus1, \
            f"FAILED: A^{expected-1} should contain zeros!"
        print(f"  ✓ A^{expected-1} has zeros (as required)")

    # Check expected IS fully positive
    is_pos = matrix_power_positive(A, expected)
    assert is_pos, f"FAILED: A^{expected} should be all positive!"
    print(f"  ✓ A^{expected} is strictly positive")

    print(f"  ✓ exp(G_{p}) = {expected}")
    return expected


# ----------------------------------------------------------------------
# 5. WORST-CASE PATH FOR p=3 (as described in the paper)
# ----------------------------------------------------------------------
def verify_worst_case_p3() -> list[int]:
    """
    Verify the explicit worst-case path for p=3:
    7 -> 6 -> 3 -> 2 -> 5 -> 0  (length 5)
    """
    p = 3
    expected_path = [7, 6, 3, 2, 5, 0]
    expected_len = 5

    adj, n = build_syracuse_graph(p)

    print(f"\n  Worst-case path 7 -> 0 for p=3:")
    print(f"    Expected: {' -> '.join(map(str, expected_path))}")

    # Verify each edge
    for i in range(len(expected_path) - 1):
        u, v = expected_path[i], expected_path[i + 1]
        assert v in adj[u], f"Invalid edge: {u} -> {v}"
    print("    ✓ All edges are valid")

    # Verify it is indeed shortest
    dist = floyd_warshall(adj, n)
    assert dist[7][0] == expected_len, \
        f"Shortest distance is {dist[7][0]}, expected {expected_len}"
    print(f"    ✓ Shortest distance confirmed: {dist[7][0]}")

    return expected_path


# ----------------------------------------------------------------------
# 6. TEST RUNNER (CLEAN & MODULAR)
# ----------------------------------------------------------------------
def print_test_header(title: str, width: int = 60):
    """Print a formatted test header."""
    print("\n" + "-" * width)
    print(f"  {title}")
    print("-" * width)


def run_tests(test_cases: list[tuple[int, int, int]]):
    """
    Run all verification tests.

    Args:
        test_cases: list of (p, expected_diameter, expected_primitivity)
    """
    width = 60

    print("=" * width)
    print("MODULAR SYRACUSE GRAPH G_p - NUMERICAL VERIFICATION")
    print("=" * width)

    for idx, (p, diam_expected, prim_expected) in enumerate(test_cases, 1):
        print_test_header(f"p = {p} (M = 2^{p} = {2**p})", width)

        # Diameter
        print(f"\n  [Diameter]")
        verify_diameter(p, diam_expected)

        # Primitivity
        print(f"\n  [Primitivity]")
        verify_primitivity(p, prim_expected)

        # Special case p=3: explicit worst-case path
        if p == 3:
            print(f"\n  [Worst-case path]")
            verify_worst_case_p3()

    # Final summary
    print("\n" + "=" * width)
    print("ALL TESTS PASSED ✓")
    print("=" * width)
    print("\nTheoretical predictions confirmed for all tested p:")
    print("  diam(G_p) = 2p - 1")
    print("  exp(G_p)  = 2p")


# ----------------------------------------------------------------------
# 7. MAIN ENTRY POINT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Define test cases: (p, expected_diameter, expected_primitivity)
    # Formula: diam = 2p - 1, exp = 2p
    TEST_CASES = [
        (2, 3, 4),   # diam = 3, exp = 4
        (3, 5, 6),   # diam = 5, exp = 6
        (4, 7, 8),   # diam = 7, exp = 8
        (5, 9, 10),  # diam = 9, exp = 10
        # Add more cases here as needed:
        # (6, 11, 12),
    ]

    run_tests(TEST_CASES)

'''
output

============================================================
MODULAR SYRACUSE GRAPH G_p - NUMERICAL VERIFICATION
============================================================

------------------------------------------------------------
  p = 2 (M = 2^2 = 4)
------------------------------------------------------------

  [Diameter]
  ✓ diam(G_2) = 3 (expected 3)
    Worst pair: (1, 3)

  [Primitivity]
  ✓ A^3 has zeros (as required)
  ✓ A^4 is strictly positive
  ✓ exp(G_2) = 4

------------------------------------------------------------
  p = 3 (M = 2^3 = 8)
------------------------------------------------------------

  [Diameter]
  ✓ diam(G_3) = 5 (expected 5)
    Worst pair: (3, 7)

  [Primitivity]
  ✓ A^5 has zeros (as required)
  ✓ A^6 is strictly positive
  ✓ exp(G_3) = 6

  [Worst-case path]

  Worst-case path 7 -> 0 for p=3:
    Expected: 7 -> 6 -> 3 -> 2 -> 5 -> 0
    ✓ All edges are valid
    ✓ Shortest distance confirmed: 5

------------------------------------------------------------
  p = 4 (M = 2^4 = 16)
------------------------------------------------------------

  [Diameter]
  ✓ diam(G_4) = 7 (expected 7)
    Worst pair: (7, 15)

  [Primitivity]
  ✓ A^7 has zeros (as required)
  ✓ A^8 is strictly positive
  ✓ exp(G_4) = 8

------------------------------------------------------------
  p = 5 (M = 2^5 = 32)
------------------------------------------------------------

  [Diameter]
  ✓ diam(G_5) = 9 (expected 9)
    Worst pair: (15, 31)

  [Primitivity]
  ✓ A^9 has zeros (as required)
  ✓ A^10 is strictly positive
  ✓ exp(G_5) = 10

============================================================
ALL TESTS PASSED ✓
============================================================

Theoretical predictions confirmed for all tested p:
  diam(G_p) = 2p - 1
  exp(G_p)  = 2p 
'''
  