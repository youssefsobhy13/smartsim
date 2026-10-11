"""Profit formulas for the newspaper seller (page 135)."""

from config.constants import PURCHASE_COST, SALVAGE_VALUE, SELLING_PRICE


def profit_demand_le_order(demand: float, Q: float, p: float = SELLING_PRICE,
                           c: float = PURCHASE_COST,
                           s: float = SALVAGE_VALUE) -> float:
    """Demand <= Q: ``demand*p + (Q - demand)*s - Q*c``.

    Example:
        >>> round(profit_demand_le_order(40, 50, 0.50, 0.33, 0.0), 2)
        3.5
    """
    if demand < 0 or Q < 0:
        raise ValueError("demand and Q must be >= 0")
    return demand * p + (Q - demand) * s - Q * c


def profit_demand_gt_order(Q: float, p: float = SELLING_PRICE,
                           c: float = PURCHASE_COST) -> float:
    """Demand > Q: ``Q*p - Q*c`` (everything ordered is sold).

    Example:
        >>> round(profit_demand_gt_order(40), 2)
        6.8
    """
    if Q < 0:
        raise ValueError("Q must be >= 0")
    return Q * p - Q * c


def profit(demand: float, Q: float, p: float = SELLING_PRICE,
           c: float = PURCHASE_COST, s: float = SALVAGE_VALUE) -> float:
    """Profit for one day choosing the right formula."""
    if demand <= Q:
        return profit_demand_le_order(demand, Q, p, c, s)
    return profit_demand_gt_order(Q, p, c)
