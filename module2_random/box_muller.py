"""Box-Muller transform for normal samples."""

import math
import random
from typing import Optional


def generate_normal(mean: float = 0.0, std: float = 1.0,
                    rng: Optional[random.Random] = None) -> float:
    """One normal sample: Z = sqrt(-2 ln U1) cos(2 pi U2).

    Args:
        mean: Mean of the result.
        std: Standard deviation (must be >= 0).
        rng: Optional ``random.Random`` for reproducibility.
    """
    if std < 0:
        raise ValueError("std must be >= 0")
    rng = rng or random.Random()
    u1 = 1.0 - rng.random()  # in (0, 1], avoids log(0)
    u2 = rng.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    return mean + std * z
