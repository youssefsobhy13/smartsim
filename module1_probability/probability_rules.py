"""Basic probability rules (classical, addition, multiplication, complement)."""

from typing import Any, Dict, Optional

from module1_probability.events import Event
from module1_probability.sample_space import SampleSpace


def check_probability(p: float, name: str = "probability") -> float:
    """Return ``p`` if it lies in [0, 1].

    Raises:
        ValueError: If ``p`` is outside [0, 1].
    """
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1, got {p}")
    return p


def classical_probability(event: Event, sample_space: SampleSpace,
                          weights: Optional[Dict[Any, float]] = None) -> float:
    """P(E) = n(E)/n(S), or the sum of outcome weights when given.

    Args:
        event: A discrete event of ``sample_space``.
        sample_space: A discrete sample space.
        weights: Optional ``{outcome: probability}`` for non-equally-likely
            outcomes (e.g. the loaded die). Weights are normalised by their
            total so ratios are accepted too.

    Example:
        >>> from module1_probability.sample_space import create_discrete_space
        >>> from module1_probability.events import define_event
        >>> die = create_discrete_space([1, 2, 3, 4, 5, 6])
        >>> classical_probability(define_event(die, lambda x: x % 2 == 0), die)
        0.5
    """
    if not sample_space.is_discrete or event.outcomes is None:
        raise ValueError("classical_probability needs a discrete space/event")
    if weights is None:
        return len(event.outcomes) / sample_space.get_size()
    if set(weights) != set(sample_space.outcomes):
        raise ValueError("weights must cover every outcome of the space")
    if any(w < 0 for w in weights.values()):
        raise ValueError("weights must be non-negative")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("weights must have a positive total")
    return sum(weights[o] for o in event.outcomes) / total


def addition_rule(P_A: float, P_B: float, P_A_and_B: float) -> float:
    """P(A U B) = P(A) + P(B) - P(A n B)."""
    for n, v in (("P_A", P_A), ("P_B", P_B), ("P_A_and_B", P_A_and_B)):
        check_probability(v, n)
    return P_A + P_B - P_A_and_B


def multiplication_rule(P_A_given_B: float, P_B: float) -> float:
    """P(A n B) = P(A|B) * P(B)."""
    check_probability(P_A_given_B, "P_A_given_B")
    check_probability(P_B, "P_B")
    return P_A_given_B * P_B


def complement_rule(P_A: float) -> float:
    """P(A') = 1 - P(A)."""
    return 1.0 - check_probability(P_A, "P_A")
