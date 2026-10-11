"""Bayes' theorem."""

from module1_probability.probability_rules import check_probability


def bayes_theorem(P_B_given_A: float, P_A: float, P_B: float) -> float:
    """P(A|B) = P(B|A) P(A) / P(B).

    Raises:
        ValueError: If ``P_B`` is 0, an input is not a probability, or the
            result exceeds 1 (inconsistent inputs).

    Example:
        >>> round(bayes_theorem(0.9, 0.01, 0.108), 4)
        0.0833
    """
    check_probability(P_B_given_A, "P_B_given_A")
    check_probability(P_A, "P_A")
    check_probability(P_B, "P_B")
    if P_B == 0:
        raise ValueError("P(B) must be > 0")
    result = P_B_given_A * P_A / P_B
    if result > 1 + 1e-12:
        raise ValueError("inconsistent inputs: P(A|B) would exceed 1")
    return min(result, 1.0)
