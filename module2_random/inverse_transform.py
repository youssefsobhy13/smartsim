"""Inverse-transform sampling."""

import math
from typing import Callable


def exponential_inverse(u: float, lam: float = 1.0) -> float:
    """X = -ln(1 - u) / lam for u in [0, 1).

    Example:
        >>> round(exponential_inverse(0.632121, 1.0), 3)
        1.0
    """
    if lam <= 0:
        raise ValueError("lam must be > 0")
    if not 0.0 <= u < 1.0:
        raise ValueError("u must be in [0, 1)")
    return -math.log(1.0 - u) / lam


def uniform_inverse(u: float, a: float, b: float) -> float:
    """X = a + (b - a) u."""
    if b < a:
        raise ValueError("b must be >= a")
    return a + (b - a) * u


def generic_inverse(u: float, inverse_cdf: Callable[[float], float]) -> float:
    """Apply any inverse CDF to ``u``."""
    return inverse_cdf(u)
