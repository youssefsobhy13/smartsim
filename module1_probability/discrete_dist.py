"""Discrete probability distribution (PMF, CDF, moments)."""

import math
import random
from typing import List, Optional, Sequence


class DiscreteDistribution:
    """Discrete random variable defined by values and probabilities.

    Args:
        values: Possible values.
        probabilities: Matching probabilities; must sum to 1.
        name: Optional label used in plots.

    Raises:
        ValueError: On length mismatch, negative probabilities, duplicate
            values, or a sum different from 1.
    """

    def __init__(self, values: Sequence[float], probabilities: Sequence[float],
                 name: str = "Discrete RV") -> None:
        if len(values) != len(probabilities) or not values:
            raise ValueError("values and probabilities need equal, non-zero length")
        if len(set(values)) != len(values):
            raise ValueError("duplicate values")
        if any(p < 0 for p in probabilities):
            raise ValueError("probabilities must be non-negative")
        if not math.isclose(sum(probabilities), 1.0, abs_tol=1e-9):
            raise ValueError(f"probabilities sum to {sum(probabilities)}, not 1")
        pairs = sorted(zip(values, probabilities))
        self.values: List[float] = [v for v, _ in pairs]
        self.probabilities: List[float] = [p for _, p in pairs]
        self.name = name

    def pmf(self, x: float) -> float:
        """P(X = x); 0 if x is not a value."""
        for v, p in zip(self.values, self.probabilities):
            if v == x:
                return p
        return 0.0

    def cdf(self, x: float) -> float:
        """P(X <= x)."""
        return sum(p for v, p in zip(self.values, self.probabilities) if v <= x)

    def mean(self) -> float:
        """E[X] = sum x f(x)."""
        return sum(v * p for v, p in zip(self.values, self.probabilities))

    def variance(self) -> float:
        """V(X) = E[X^2] - (E[X])^2."""
        ex2 = sum(v * v * p for v, p in zip(self.values, self.probabilities))
        return ex2 - self.mean() ** 2

    def std(self) -> float:
        """Standard deviation."""
        return math.sqrt(self.variance())

    def sample(self, n: int = 1, seed: Optional[int] = None) -> List[float]:
        """Draw ``n`` values (reproducible with ``seed``)."""
        rng = random.Random(seed)
        return rng.choices(self.values, weights=self.probabilities, k=n)
