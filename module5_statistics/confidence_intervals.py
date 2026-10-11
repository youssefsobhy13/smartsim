"""Confidence intervals."""

import math
from typing import Sequence, Tuple

import numpy as np
from scipy import stats


def mean_ci(data: Sequence[float], confidence: float = 0.95) -> Tuple[float, float]:
    """t-based interval ``x_bar +/- t * s / sqrt(n)`` for the mean.

    Args:
        data: At least two observations.
        confidence: Confidence level in (0, 1).

    Returns:
        ``(low, high)``.

    Example:
        >>> low, high = mean_ci([3.0, 4.0, 3.5, 3.6, 3.4])
        >>> low < 3.5 < high
        True
    """
    x = np.asarray(data, dtype=float)
    if x.size < 2:
        raise ValueError("need at least 2 observations")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be in (0, 1)")
    m = x.mean()
    se = x.std(ddof=1) / math.sqrt(x.size)
    if se == 0:
        return float(m), float(m)
    t = stats.t.ppf((1 + confidence) / 2, df=x.size - 1)
    return float(m - t * se), float(m + t * se)


def proportion_ci(successes: int, n: int,
                  confidence: float = 0.95) -> Tuple[float, float]:
    """Wilson score interval for a proportion (e.g. the service level).

    Raises:
        ValueError: If ``n`` <= 0 or ``successes`` is outside [0, n].
    """
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("need n > 0 and 0 <= successes <= n")
    z = stats.norm.ppf((1 + confidence) / 2)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)
