"""Factories for discrete and continuous random variables."""

from typing import Callable, Sequence, Tuple

from module1_probability.continuous_dist import ContinuousDistribution
from module1_probability.discrete_dist import DiscreteDistribution


def discrete_rv(values: Sequence[float],
                probabilities: Sequence[float]) -> DiscreteDistribution:
    """Build a discrete RV; probabilities must sum to 1.

    Example:
        >>> discrete_rv([0, 1, 2], [0.25, 0.5, 0.25]).mean()
        1.0
    """
    return DiscreteDistribution(values, probabilities)


def continuous_rv(pdf_func: Callable[[float], float],
                  support: Tuple[float, float]) -> ContinuousDistribution:
    """Build a continuous RV from a PDF and its support."""
    return ContinuousDistribution(pdf_func, support)
