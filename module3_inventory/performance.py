"""Performance metrics computed from an inventory ``history``."""

from typing import Dict, List, Optional

from config.constants import (HOLDING_COST_PER_UNIT_DAY,
                              ORDERING_COST_PER_ORDER, SHORTAGE_COST_PER_UNIT)
from module3_inventory.shortage_analysis import (calculate_shortage_rate,
                                                 count_shortage_days)

History = List[dict]


def total_ending_inventory(history: History) -> int:
    """Sum of the ending inventory of every day."""
    return sum(r["end"] for r in history)


def average_inventory(history: History) -> float:
    """Sum(ending inventory) / number of days."""
    if not history:
        raise ValueError("empty history")
    return total_ending_inventory(history) / len(history)


def service_level(history: History) -> float:
    """1 - shortage rate (a fraction, 0.92 means 92%)."""
    return 1.0 - calculate_shortage_rate(history)


def total_cost(history: History, costs: Optional[Dict[str, float]] = None) -> float:
    """Holding + ordering + shortage cost.

    Args:
        history: Inventory history.
        costs: Optional dict with ``holding`` (per unit-day), ``ordering``
            (per order) and ``shortage`` (per unit). Missing keys fall back to
            the ASSUMED rates in ``config/constants.py``.
    """
    c = {"holding": HOLDING_COST_PER_UNIT_DAY, "ordering": ORDERING_COST_PER_ORDER,
         "shortage": SHORTAGE_COST_PER_UNIT}
    c.update(costs or {})
    holding = c["holding"] * total_ending_inventory(history)
    ordering = c["ordering"] * sum(1 for r in history if r.get("order_qty"))
    shortage = c["shortage"] * sum(r["shortage"] for r in history)
    return holding + ordering + shortage


def compute_metrics(history: History) -> Dict[str, float]:
    """All headline metrics in one dict."""
    return {
        "days": len(history),
        "total_ending_inventory": total_ending_inventory(history),
        "average_inventory": average_inventory(history),
        "shortage_days": count_shortage_days(history),
        "shortage_rate": calculate_shortage_rate(history),
        "service_level": service_level(history),
        "shortage_units": sum(r["shortage"] for r in history),
    }
