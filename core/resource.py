"""A server with limited capacity and a FIFO waiting queue."""

from typing import Any, Callable, Optional

from core.queue import Queue


class Resource:
    """Resource with ``capacity`` servers.

    Args:
        capacity: Number of entities served at the same time.
        on_start: Optional callback ``on_start(entity)`` called whenever an
            entity begins service (immediately or after waiting).
    """

    def __init__(self, capacity: int = 1,
                 on_start: Optional[Callable[[Any], None]] = None) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.in_service = 0
        self.queue = Queue()
        self.on_start = on_start

    def request(self, entity: Any) -> bool:
        """Start service if a server is free, otherwise join the queue.

        Returns:
            True if service started immediately, False if the entity waits.
        """
        if self.in_service < self.capacity:
            self._start(entity)
            return True
        self.queue.enqueue(entity)
        return False

    def release(self) -> None:
        """Free one server and start the next waiting entity (if any)."""
        if self.in_service == 0:
            raise RuntimeError("release() without an active service")
        self.in_service -= 1
        if len(self.queue) > 0:
            self._start(self.queue.dequeue())

    def _start(self, entity: Any) -> None:
        self.in_service += 1
        if self.on_start is not None:
            self.on_start(entity)
