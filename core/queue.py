"""FIFO queue.

Note: this module is named ``queue.py`` as requested. It never clashes with
the standard library because it is always imported as ``core.queue``; do not
run scripts from inside the ``core/`` folder.
"""

from collections import deque
from typing import Any, Deque


class Queue:
    """First-in first-out waiting line."""

    def __init__(self) -> None:
        self._items: Deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Add an item at the back."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item.

        Raises:
            IndexError: If the queue is empty.
        """
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)
