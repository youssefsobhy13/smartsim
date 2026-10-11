"""Simulation events ordered by (time, priority, insertion order)."""

from dataclasses import dataclass, field
from typing import Callable


@dataclass(order=True)
class Event:
    """A scheduled callback.

    Ordering uses ``(time, priority, seq)`` so ties are broken first by
    priority (lower runs first) and then by insertion order.

    Args:
        time: Simulation time at which the event fires.
        priority: Tie-breaker, lower value first.
        seq: Insertion counter, assigned by the engine.
        callback: Function called with no arguments when the event fires.
    """

    time: float
    priority: int = 0
    seq: int = 0
    callback: Callable[[], None] = field(compare=False, default=lambda: None)
