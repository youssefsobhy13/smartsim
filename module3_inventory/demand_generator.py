"""Demand generation wrapper around the random-digit table."""

from typing import Optional

from module2_random.random_digits import map_to_demand


def generate_demand(rd: Optional[int] = None) -> int:
    """Daily demand (0-4) for random digit ``rd`` (random if ``None``)."""
    return map_to_demand(rd)
