"""Hypothesis tests."""

from typing import Sequence, Tuple

import numpy as np
from scipy import stats


def t_test(sample: Sequence[float], mu: float) -> Tuple[float, float]:
    """One-sample t-test of ``H0: mean == mu``.

    Returns:
        ``(t statistic, two-sided p-value)``.
    """
    x = np.asarray(sample, dtype=float)
    if x.size < 2:
        raise ValueError("need at least 2 observations")
    res = stats.ttest_1samp(x, mu)
    return float(res.statistic), float(res.pvalue)


def chi_square_test(observed: Sequence[float],
                    expected: Sequence[float]) -> Tuple[float, float]:
    """Chi-square goodness of fit.

    ``expected`` is rescaled to the total of ``observed`` so probabilities
    (summing to 1) are accepted as well as counts.

    Returns:
        ``(chi2 statistic, p-value)``.
    """
    obs = np.asarray(observed, dtype=float)
    exp = np.asarray(expected, dtype=float)
    if obs.shape != exp.shape or obs.size < 2:
        raise ValueError("observed and expected need the same length (>= 2)")
    if (exp <= 0).any():
        raise ValueError("expected values must be > 0")
    exp = exp * obs.sum() / exp.sum()
    res = stats.chisquare(obs, exp)
    return float(res.statistic), float(res.pvalue)
