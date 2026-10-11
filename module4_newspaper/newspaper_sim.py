"""Newspaper seller (newsvendor) simulation."""

from typing import Any, Dict, List, Optional, Sequence, Tuple

from config.constants import (NEWSPAPER_RDS, PURCHASE_COST, SALVAGE_VALUE,
                              SELLING_PRICE)
from module2_random.lcg import LinearCongruentialGenerator
from module2_random.random_digits import map_to_newsday, newsday_demand
from module4_newspaper.profit_calc import profit

Row = Dict[str, Any]


class NewspaperSeller:
    """One seller ordering ``order_qty`` papers every day.

    Args:
        order_qty: Papers bought each day.
        cost: Purchase cost per paper.
        price: Selling price per paper.
        salvage: Value of an unsold paper.
    """

    def __init__(self, order_qty: int, cost: float = PURCHASE_COST,
                 price: float = SELLING_PRICE,
                 salvage: float = SALVAGE_VALUE) -> None:
        if order_qty < 0:
            raise ValueError("order_qty must be >= 0")
        self.order_qty = order_qty
        self.cost, self.price, self.salvage = cost, price, salvage
        self.rows: List[Row] = []

    def get_newsday(self, rd: Optional[int] = None) -> Tuple[str, int]:
        """``(type, demand)`` for a random digit (page 134)."""
        kind = map_to_newsday(rd)
        return kind, newsday_demand(kind)

    def calculate_profit(self, demand: int) -> float:
        """Profit for one day with this order quantity."""
        return profit(demand, self.order_qty, self.price, self.cost, self.salvage)

    def simulate_day(self, day_num: int, rd: Optional[int] = None) -> Row:
        """One row: RD, type, demand, sold, revenue, cost, profit."""
        kind, demand = self.get_newsday(rd)
        sold = min(demand, self.order_qty)
        revenue = sold * self.price + (self.order_qty - sold) * self.salvage
        cost = self.order_qty * self.cost
        row = {"day": day_num, "rd": rd, "newsday": kind, "demand": demand,
               "sold": sold, "revenue": revenue, "cost": cost,
               "profit": self.calculate_profit(demand)}
        self.rows.append(row)
        return row

    def simulate(self, num_days: Optional[int] = None,
                 rds: Optional[Sequence[int]] = None, seed: int = 2025) -> List[Row]:
        """Simulate days with fixed ``rds`` (default: the plan's 10 RDs) or,
        if ``num_days`` is given without ``rds``, with an LCG seeded by ``seed``.
        """
        self.rows = []
        if rds is None and num_days is None:
            rds = NEWSPAPER_RDS
        if rds is None:
            gen = LinearCongruentialGenerator(seed=seed)
            rds = [gen.next_digit() for _ in range(num_days)]
        elif num_days is not None:
            rds = list(rds)[:num_days]
        for i, rd in enumerate(rds, start=1):
            self.simulate_day(i, rd)
        return self.rows

    def average_profit(self) -> float:
        """Mean daily profit of the simulated rows."""
        if not self.rows:
            raise ValueError("run simulate() first")
        return sum(r["profit"] for r in self.rows) / len(self.rows)
