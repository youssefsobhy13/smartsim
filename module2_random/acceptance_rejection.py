"""Acceptance-rejection sampling."""

import random
from typing import Callable, Optional, Tuple


def accept_reject(pdf: Callable[[float], float], max_pdf: float,
                  support: Tuple[float, float],
                  rng: Optional[random.Random] = None,
                  max_tries: int = 100000) -> float:
    """Return one sample from ``pdf`` on a bounded ``support``.

    Draw x ~ U(a, b) and y ~ U(0, max_pdf); accept x if y <= pdf(x).

    Args:
        pdf: Density (must satisfy pdf(x) <= max_pdf on the support).
        max_pdf: Upper bound of the density.
        support: Finite ``(a, b)``.
        rng: Optional ``random.Random`` for reproducibility.
        max_tries: Safety limit.

    Raises:
        RuntimeError: If no sample is accepted within ``max_tries``.
    """
    a, b = support
    rng = rng or random.Random()
    for _ in range(max_tries):
        x = rng.uniform(a, b)
        if rng.uniform(0, max_pdf) <= pdf(x):
            return x
    raise RuntimeError("accept_reject: max_tries exceeded; check max_pdf")
