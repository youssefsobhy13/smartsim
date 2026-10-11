"""Sample spaces: discrete (countable) and continuous (interval)."""

import math
from itertools import product
from typing import Any, Iterable, Optional, Tuple


class SampleSpace:
    """A set of all possible outcomes of a random experiment.

    Use :func:`create_discrete_space` or :func:`create_continuous_space`
    instead of calling the constructor directly.
    """

    def __init__(self, outcomes: Optional[Tuple[Any, ...]] = None,
                 interval: Optional[Tuple[float, float]] = None) -> None:
        self._ordered = tuple(outcomes) if outcomes is not None else None
        self.outcomes = frozenset(outcomes) if outcomes is not None else None
        self.interval = interval

    @property
    def is_discrete(self) -> bool:
        """True for a finite sample space."""
        return self.outcomes is not None

    def contains(self, x: Any) -> bool:
        """Whether ``x`` is an outcome of this space."""
        if self.is_discrete:
            return x in self.outcomes
        lo, hi = self.interval
        try:
            return lo < x < hi
        except TypeError:
            return False

    def get_size(self) -> float:
        """Number of outcomes (``float('inf')`` for a continuous space)."""
        return len(self.outcomes) if self.is_discrete else float("inf")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SampleSpace):
            return NotImplemented
        return self.outcomes == other.outcomes and self.interval == other.interval

    def __hash__(self) -> int:
        return hash((self.outcomes, self.interval))

    def __repr__(self) -> str:
        if self.is_discrete:
            return "S = {" + ", ".join(str(o) for o in self._ordered) + "}"
        lo, hi = self.interval
        if math.isinf(hi) and not math.isinf(lo):
            return f"S = {{x | x > {lo:g}}}"
        if math.isinf(lo) and not math.isinf(hi):
            return f"S = {{x | x < {hi:g}}}"
        return f"S = {{x | {lo:g} < x < {hi:g}}}"


def create_discrete_space(outcomes: Iterable[Any]) -> SampleSpace:
    """Create a finite sample space.

    Args:
        outcomes: Iterable of distinct outcomes.

    Returns:
        A discrete :class:`SampleSpace`.

    Raises:
        ValueError: If ``outcomes`` is empty or has duplicates.

    Example:
        >>> create_discrete_space([1, 2, 3, 4, 5, 6])
        S = {1, 2, 3, 4, 5, 6}
    """
    items = tuple(outcomes)
    if not items:
        raise ValueError("a sample space cannot be empty")
    if len(set(items)) != len(items):
        raise ValueError("duplicate outcomes are not allowed")
    return SampleSpace(outcomes=items)


def create_continuous_space(interval: Tuple[float, float]) -> SampleSpace:
    """Create a continuous space described by an open interval.

    Args:
        interval: ``(low, high)``; use ``float('inf')`` for unbounded.

    Example:
        >>> create_continuous_space((0, float('inf')))
        S = {x | x > 0}
    """
    lo, hi = interval
    if not lo < hi:
        raise ValueError("interval must satisfy low < high")
    return SampleSpace(interval=(lo, hi))


def product_space(*spaces: SampleSpace, join: bool = True) -> SampleSpace:
    """Cartesian product of discrete spaces (tree diagram, page 10).

    Args:
        spaces: Two or more discrete spaces.
        join: If True and all outcomes are strings, concatenate them
            (``'H'`` x ``'T'`` -> ``'HT'``); otherwise use tuples.

    Example:
        >>> coin = create_discrete_space(['H', 'T'])
        >>> product_space(coin, coin)
        S = {HH, HT, TH, TT}
    """
    if not spaces or not all(s.is_discrete for s in spaces):
        raise ValueError("product_space needs one or more discrete spaces")
    combos = product(*(s._ordered for s in spaces))
    if join and all(isinstance(o, str) for s in spaces for o in s._ordered):
        return create_discrete_space(["".join(c) for c in combos])
    return create_discrete_space(list(combos))
