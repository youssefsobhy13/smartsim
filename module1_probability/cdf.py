"""Step-function CDF table for a discrete random variable."""

from typing import List, Tuple

from module1_probability.discrete_dist import DiscreteDistribution


def cumulative_distribution(dist: DiscreteDistribution) -> List[Tuple[float, float]]:
    """Return the CDF table ``[(x, F(x)), ...]``.

    Example:
        >>> from module1_probability.random_variables import discrete_rv
        >>> cumulative_distribution(discrete_rv([0, 1, 2], [0.25, 0.5, 0.25]))
        [(0, 0.25), (1, 0.75), (2, 1.0)]
    """
    table: List[Tuple[float, float]] = []
    running = 0.0
    for v, p in zip(dist.values, dist.probabilities):
        running += p
        table.append((v, min(round(running, 12), 1.0)))
    return table
