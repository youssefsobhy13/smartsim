"""Law of large numbers and central limit theorem demonstrations."""

from typing import Callable, Optional

import numpy as np

Sampler = Callable[[np.random.Generator, int], np.ndarray]


def _exponential(rng: np.random.Generator, size: int) -> np.ndarray:
    return rng.exponential(1.0, size)


def law_of_large_numbers(n: int = 1000, sampler: Optional[Sampler] = None,
                         seed: int = 2025) -> np.ndarray:
    """Running mean after 1, 2, ..., n draws (data for the convergence plot).

    The default sampler is Exponential(1) whose true mean is 1.
    """
    rng = np.random.default_rng(seed)
    x = (sampler or _exponential)(rng, n)
    return np.cumsum(x) / np.arange(1, n + 1)


def central_limit_theorem(n: int = 30, replications: int = 2000,
                          sampler: Optional[Sampler] = None, mean: float = 1.0,
                          std: float = 1.0, seed: int = 2025) -> np.ndarray:
    """Standardised sums ``(S_n - n mu) / (sigma sqrt(n))`` for a histogram.

    Args:
        n: Draws per sum (n >= 30 for a good normal approximation).
        replications: Number of sums.
        sampler: ``f(rng, size)``; default Exponential(1) (mean 1, std 1).
        mean, std: True mean and std of the sampler.
    """
    if n < 1 or replications < 1:
        raise ValueError("n and replications must be >= 1")
    rng = np.random.default_rng(seed)
    draws = (sampler or _exponential)(rng, n * replications).reshape(replications, n)
    return (draws.sum(axis=1) - n * mean) / (std * np.sqrt(n))
