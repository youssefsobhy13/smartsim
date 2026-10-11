"""Events as subsets of a sample space, plus set operations."""

from typing import Any, Callable, FrozenSet, Optional

from module1_probability.sample_space import SampleSpace


class Event:
    """A subset of a sample space (discrete or described by a predicate)."""

    def __init__(self, space: SampleSpace,
                 outcomes: Optional[FrozenSet[Any]] = None,
                 predicate: Optional[Callable[[Any], bool]] = None) -> None:
        self.space = space
        self.outcomes = outcomes
        self._predicate = predicate

    def contains(self, x: Any) -> bool:
        """Whether outcome ``x`` belongs to the event."""
        if self.outcomes is not None:
            return x in self.outcomes
        return self.space.contains(x) and bool(self._predicate(x))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return NotImplemented
        return self.space == other.space and self.outcomes == other.outcomes \
            if self.outcomes is not None else self is other

    def __hash__(self) -> int:
        return hash((self.space, self.outcomes))

    def __repr__(self) -> str:
        if self.outcomes is None:
            return "E = {x | condition(x)}"
        try:
            items = sorted(self.outcomes)
        except TypeError:
            items = sorted(self.outcomes, key=str)
        return "E = {" + ", ".join(str(i) for i in items) + "}"


def define_event(sample_space: SampleSpace,
                 condition: Callable[[Any], bool]) -> Event:
    """All outcomes of the space that satisfy ``condition(x)``.

    Example:
        >>> from module1_probability.sample_space import create_discrete_space
        >>> die = create_discrete_space([1, 2, 3, 4, 5, 6])
        >>> define_event(die, lambda x: x % 2 == 0)
        E = {2, 4, 6}
    """
    if sample_space.is_discrete:
        return Event(sample_space,
                     outcomes=frozenset(o for o in sample_space.outcomes
                                        if condition(o)))
    return Event(sample_space, predicate=condition)


def is_subset(event: Event, sample_space: SampleSpace) -> bool:
    """True if every outcome of ``event`` is in ``sample_space``.

    For continuous events the check is structural: the event must have been
    defined on that same space.
    """
    if event.outcomes is not None:
        return all(sample_space.contains(o) for o in event.outcomes)
    return event.space == sample_space


def _check_same_space(a: Event, b: Event) -> None:
    if a.space != b.space:
        raise ValueError("events must belong to the same sample space")


def union(a: Event, b: Event) -> Event:
    """A U B."""
    _check_same_space(a, b)
    if a.outcomes is not None and b.outcomes is not None:
        return Event(a.space, outcomes=a.outcomes | b.outcomes)
    return Event(a.space, predicate=lambda x: a.contains(x) or b.contains(x))


def intersection(a: Event, b: Event) -> Event:
    """A n B."""
    _check_same_space(a, b)
    if a.outcomes is not None and b.outcomes is not None:
        return Event(a.space, outcomes=a.outcomes & b.outcomes)
    return Event(a.space, predicate=lambda x: a.contains(x) and b.contains(x))


def complement(a: Event) -> Event:
    """Outcomes of the parent space that are not in ``a``."""
    if a.outcomes is not None:
        return Event(a.space, outcomes=a.space.outcomes - a.outcomes)
    return Event(a.space, predicate=lambda x: not a.contains(x))
