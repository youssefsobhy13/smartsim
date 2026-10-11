"""Shortage analysis.

A shortage day is a day on which demand was NOT fully served. A day that
ends with 0 units but served all demand is not a shortage (page 78).
"""

from typing import Dict, List

History = List[dict]


def count_shortage_days(history: History) -> int:
    """Number of days with unserved demand."""
    return sum(1 for r in history if r["shortage"] > 0)


def calculate_shortage_rate(history: History) -> float:
    """Shortage days / total days."""
    if not history:
        raise ValueError("empty history")
    return count_shortage_days(history) / len(history)


def analyze_shortage_patterns(history: History) -> Dict[str, object]:
    """Where shortages occur.

    Returns:
        Dict with ``days`` (list of ``(cycle, day, units)``), ``total_units``
        and ``per_cycle`` (cycle -> units).
    """
    days = [(r["cycle"], r["day"], r["shortage"]) for r in history if r["shortage"] > 0]
    per_cycle: Dict[int, int] = {}
    for cyc, _day, units in days:
        per_cycle[cyc] = per_cycle.get(cyc, 0) + units
    return {"days": days, "total_units": sum(u for _c, _d, u in days),
            "per_cycle": per_cycle}
