"""Conditional probability and independence."""

import math

from module1_probability.probability_rules import check_probability


def conditional_probability(P_A_and_B: float, P_A: float) -> float:
    """P(B|A) = P(A n B) / P(A).

    Raises:
        ValueError: If ``P_A`` is 0 or an input is not a probability.
    """
    check_probability(P_A_and_B, "P_A_and_B")
    check_probability(P_A, "P_A")
    if P_A == 0:
        raise ValueError("P(A) must be > 0 for a conditional probability")
    return P_A_and_B / P_A


def independence_check(P_A: float, P_B: float, P_A_and_B: float) -> bool:
    """True if P(A n B) is approximately P(A) * P(B)."""
    for n, v in (("P_A", P_A), ("P_B", P_B), ("P_A_and_B", P_A_and_B)):
        check_probability(v, n)
    return math.isclose(P_A_and_B, P_A * P_B, rel_tol=1e-9, abs_tol=1e-12)
