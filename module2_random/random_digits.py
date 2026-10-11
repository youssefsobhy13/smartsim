"""Random-digit lookup tables (demand, lead time, newsday).

Boundary rules: demand range 92-00 means 92..99 and 00 (00 counts as 100);
lead time uses one digit and digit 0 counts as 10.
"""

import random
from typing import Optional, Tuple

from config.constants import (DEMAND_RD_RANGES, LEAD_TIME_RD_RANGES,
                              NEWSDAY_TABLE)

_rng = random.Random()


def generate_digit(rng: Optional[random.Random] = None,
                   seed: Optional[int] = None) -> int:
    """Random two-digit number 0-99.

    Args:
        rng: Optional generator to draw from.
        seed: If given (and no ``rng``), reseed the module generator first.
    """
    if rng is None:
        if seed is not None:
            _rng.seed(seed)
        rng = _rng
    return rng.randint(0, 99)


def map_to_demand(digit: Optional[int] = None) -> int:
    """Demand 0-4 from a two-digit RD (page 86). Random digit if ``None``."""
    d = generate_digit() if digit is None else digit
    if not 0 <= d <= 99:
        raise ValueError("demand digit must be 0-99")
    d = 100 if d == 0 else d
    for lo, hi, value in DEMAND_RD_RANGES:
        if lo <= d <= hi:
            return value
    raise ValueError(f"no demand range for digit {digit}")


def map_to_lead_time(digit: Optional[int] = None) -> int:
    """Lead time 1-3 days from a single digit (page 88)."""
    d = random.Random().randint(0, 9) if digit is None else digit
    if not 0 <= d <= 9:
        raise ValueError("lead-time digit must be 0-9")
    d = 10 if d == 0 else d
    for lo, hi, value in LEAD_TIME_RD_RANGES:
        if lo <= d <= hi:
            return value
    raise ValueError(f"no lead-time range for digit {digit}")


def map_to_newsday(digit: Optional[int] = None) -> str:
    """'Good', 'Fair' or 'Poor' from a two-digit RD (page 134)."""
    d = generate_digit() if digit is None else digit
    if not 0 <= d <= 99:
        raise ValueError("newsday digit must be 0-99")
    for name, _p, _dem, lo, hi in NEWSDAY_TABLE:
        if lo <= d <= hi:
            return name
    raise ValueError(f"no newsday range for digit {digit}")


def newsday_demand(newsday: str) -> int:
    """Newspaper demand for a day type: Good 40, Fair 50, Poor 60."""
    for name, _p, demand, _lo, _hi in NEWSDAY_TABLE:
        if name == newsday:
            return demand
    raise ValueError(f"unknown newsday type {newsday!r}")


def newsday_with_demand(digit: Optional[int] = None) -> Tuple[str, int]:
    """Convenience: ``(type, demand)`` for an RD."""
    kind = map_to_newsday(digit)
    return kind, newsday_demand(kind)
