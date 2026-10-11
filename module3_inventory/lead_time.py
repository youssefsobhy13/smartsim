"""Lead-time generation wrapper around the random-digit table."""

from typing import Optional

from module2_random.random_digits import map_to_lead_time


def generate_lead_time(rd: Optional[int] = None) -> int:
    """Lead time in days (1-3) for single digit ``rd`` (random if ``None``)."""
    return map_to_lead_time(rd)
