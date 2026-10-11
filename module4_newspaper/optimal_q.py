"""Compare order quantities and find the best one."""

from typing import Dict, Optional, Sequence

from config.constants import NEWSDAY_TABLE, NEWSPAPER_RDS, ORDER_QUANTITIES
from module4_newspaper.newspaper_sim import NewspaperSeller
from module4_newspaper.profit_calc import profit


def test_order_quantities(quantities: Sequence[int] = tuple(ORDER_QUANTITIES),
                          rds: Optional[Sequence[int]] = None,
                          num_days: Optional[int] = None,
                          seed: int = 2025) -> Dict[int, float]:
    """Average daily profit for each order quantity (``{Q: profit}``).

    Uses the plan's 10 fixed RDs unless ``rds`` or ``num_days`` is given.
    """
    if rds is None and num_days is None:
        rds = NEWSPAPER_RDS
    result = {}
    for q in quantities:
        seller = NewspaperSeller(q)
        seller.simulate(num_days=num_days, rds=rds, seed=seed)
        result[q] = seller.average_profit()
    return result


test_order_quantities.__test__ = False  # not a pytest test


def find_optimal(profits: Optional[Dict[int, float]] = None) -> int:
    """Order quantity with the highest average profit."""
    profits = profits or test_order_quantities()
    return max(profits, key=profits.get)


def analytic_expected_profit(Q: int, newsday_table=NEWSDAY_TABLE) -> float:
    """Exact expected daily profit: sum of P(type) * profit(demand, Q).

    Example:
        >>> [round(analytic_expected_profit(q), 2) for q in (40, 50, 60)]
        [6.8, 6.75, 4.45]
    """
    return sum(p * profit(demand, Q) for _n, p, demand, _lo, _hi in newsday_table)
