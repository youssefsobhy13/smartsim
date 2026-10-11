"""Generic discrete-event simulation engine (no SimPy inside)."""

import heapq
from typing import Callable, List, Optional

from core.event import Event


class SimulationEngine:
    """Clock plus a heap of events.

    Example:
        >>> eng = SimulationEngine()
        >>> out = []
        >>> _ = eng.schedule(2, lambda: out.append(eng.now))
        >>> eng.run()
        >>> out
        [2.0]
    """

    def __init__(self) -> None:
        self.now: float = 0.0
        self._heap: List[Event] = []
        self._counter = 0
        self._stopped = False

    def schedule(self, delay: float, callback: Callable[[], None],
                 priority: int = 0) -> Event:
        """Insert an event at ``now + delay``.

        Raises:
            ValueError: If ``delay`` is negative.
        """
        if delay < 0:
            raise ValueError("delay must be >= 0")
        self._counter += 1
        ev = Event(self.now + delay, priority, self._counter, callback)
        heapq.heappush(self._heap, ev)
        return ev

    def run(self, until: Optional[float] = None) -> None:
        """Pop events in time order, advance the clock and call them."""
        self._stopped = False
        while self._heap and not self._stopped:
            if until is not None and self._heap[0].time > until:
                self.now = float(until)
                return
            ev = heapq.heappop(self._heap)
            self.now = ev.time
            ev.callback()

    def stop(self) -> None:
        """Stop the run loop after the current event."""
        self._stopped = True

    def pending(self) -> int:
        """Number of events still waiting."""
        return len(self._heap)
