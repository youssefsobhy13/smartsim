"""Continuous probability distribution (PDF, CDF, probabilities, mean)."""

import math
from typing import Callable, Optional, Tuple

from scipy.integrate import quad


class ContinuousDistribution:
    """Continuous random variable from a PDF and its support.

    Args:
        pdf_func: Density function.
        support: ``(low, high)``; ``high`` may be ``float('inf')``.
        cdf_func: Optional closed-form CDF (used instead of integration).
        name: Optional label used in plots.
    """

    def __init__(self, pdf_func: Callable[[float], float],
                 support: Tuple[float, float],
                 cdf_func: Optional[Callable[[float], float]] = None,
                 name: str = "Continuous RV") -> None:
        lo, hi = support
        if not lo < hi:
            raise ValueError("support must satisfy low < high")
        self._pdf = pdf_func
        self.support = (lo, hi)
        self._cdf = cdf_func
        self.name = name

    def pdf(self, x: float) -> float:
        """Density at ``x`` (0 outside the support)."""
        lo, hi = self.support
        return self._pdf(x) if lo <= x <= hi else 0.0

    def cdf(self, x: float) -> float:
        """F(x) = P(X <= x)."""
        lo, hi = self.support
        if x <= lo:
            return 0.0
        if self._cdf is not None:
            return 1.0 if x >= hi else self._cdf(x)
        upper = min(x, hi)
        value, _ = quad(self._pdf, lo, upper)
        return min(1.0, value)

    def probability(self, a: float, b: float) -> float:
        """P(a <= X <= b) = F(b) - F(a)."""
        if a > b:
            raise ValueError("a must be <= b")
        return self.cdf(b) - self.cdf(a)

    def mean(self) -> float:
        """E[X] = integral of x f(x)."""
        lo, hi = self.support
        value, _ = quad(lambda x: x * self._pdf(x), lo, hi)
        return value


def exponential_rv(lam: float = 1.0) -> ContinuousDistribution:
    """Exponential distribution f(x) = lam e^(-lam x), x > 0.

    Example:
        >>> round(exponential_rv(1).cdf(1), 6)
        0.632121
    """
    if lam <= 0:
        raise ValueError("lam must be > 0")
    return ContinuousDistribution(
        lambda x: lam * math.exp(-lam * x), (0.0, float("inf")),
        cdf_func=lambda x: 1.0 - math.exp(-lam * x),
        name=f"Exponential(lambda={lam:g})")
