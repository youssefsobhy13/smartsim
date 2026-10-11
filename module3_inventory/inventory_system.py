"""(M,N) periodic-review inventory simulation.

Every ``N`` days the stock is reviewed and an order is placed to bring the
inventory position back up to ``M``. Orders arrive after a random lead time,
at the start of absolute day ``review_day + lead_time`` (the initial pending
order of 8 units "arrives in 2 days", i.e. at the start of day 2).
Unserved demand is carried as backorder and served first when stock arrives.

History format (one dict per simulated day, frozen for Persons 7, 9, 10)::

    {"cycle", "day", "abs_day", "begin", "rd_demand", "demand", "end",
     "shortage", "order_qty", "lead_time", "note"}

``begin`` is the stock available at the start of the day after arrivals and
backorder clearing. Extra keys ``arrival`` and ``backorder`` are additive.
"""

from typing import Any, Dict, List, Optional, Sequence, Tuple

from module3_inventory.demand_generator import generate_demand
from module3_inventory.lead_time import generate_lead_time

Row = Dict[str, Any]


class InventorySystemMN:
    """Simulates the (M,N) inventory system.

    Args:
        M: Maximum inventory level.
        N: Review period in days.
        initial: Initial inventory.
        pending: ``(units, arrival_day)`` of the order already on its way,
            or ``None``.
        demand_shift: Added to every demand (sensitivity analysis), floored at 0.
        lead_shift: Added to every lead time (sensitivity analysis), min 1.
    """

    def __init__(self, M: int = 11, N: int = 5, initial: int = 3,
                 pending: Optional[Tuple[int, int]] = (8, 2),
                 demand_shift: int = 0, lead_shift: int = 0) -> None:
        if M < 1 or N < 1:
            raise ValueError("M and N must be >= 1")
        self.M, self.N = M, N
        self.inventory = initial
        self.backorder = 0
        self.demand_shift = demand_shift
        self.lead_shift = lead_shift
        self.abs_day = 0
        self.history: List[Row] = []
        self._pending: List[Tuple[int, int]] = []
        if pending and pending[0] > 0:
            self._pending.append((pending[1], pending[0]))  # (arrival_day, qty)

    # -- lookups -----------------------------------------------------------
    def get_demand(self, rd: Optional[int] = None) -> int:
        """Demand for a random digit (table on page 86)."""
        return max(0, generate_demand(rd) + self.demand_shift)

    def get_lead_time(self, rd: Optional[int] = None) -> int:
        """Lead time for a random digit (table on page 88)."""
        return max(1, generate_lead_time(rd) + self.lead_shift)

    # -- one day -----------------------------------------------------------
    def run_day(self, demand_rd: Optional[int] = None) -> Row:
        """Simulate one day and append a row to ``history``."""
        self.abs_day += 1
        cycle = (self.abs_day - 1) // self.N + 1
        day = (self.abs_day - 1) % self.N + 1

        arrival = sum(q for d, q in self._pending if d == self.abs_day)
        self._pending = [(d, q) for d, q in self._pending if d != self.abs_day]
        self.inventory += arrival
        cleared = min(self.inventory, self.backorder)
        self.inventory -= cleared
        self.backorder -= cleared
        begin = self.inventory

        demand = self.get_demand(demand_rd)
        served = min(self.inventory, demand)
        shortage = demand - served
        self.inventory -= served
        self.backorder += shortage

        note = ""
        if arrival:
            note = "Arrived"
        if shortage:
            note = f"Shortage {self.backorder}"
        row: Row = {
            "cycle": cycle, "day": day, "abs_day": self.abs_day,
            "begin": begin, "rd_demand": demand_rd, "demand": demand,
            "end": self.inventory, "shortage": shortage,
            "order_qty": None, "lead_time": None, "note": note,
            "arrival": arrival, "backorder": self.backorder,
        }
        self.history.append(row)
        return row

    def place_order(self, lead_time_rd: Optional[int] = None) -> Tuple[int, int]:
        """On a review day, order up to M and schedule the arrival.

        Returns:
            ``(order_qty, lead_time)``. Also recorded on the last history row.
        """
        in_transit = sum(q for _d, q in self._pending)
        qty = max(0, self.M - (self.inventory - self.backorder + in_transit))
        lead = self.get_lead_time(lead_time_rd)
        if qty > 0:
            self._pending.append((self.abs_day + lead, qty))
        last = self.history[-1]
        last["order_qty"], last["lead_time"] = qty, lead
        extra = f"Order {qty}, LT {lead}"
        last["note"] = f"{last['note']}; {extra}" if last["note"] else extra
        return qty, lead

    # -- cycles ------------------------------------------------------------
    def run_cycles(self, num_cycles: int,
                   demand_rds: Optional[Sequence[int]] = None,
                   lead_time_rds: Optional[Sequence[int]] = None,
                   rng: Any = None) -> List[Row]:
        """Run ``num_cycles`` cycles of ``N`` days.

        Args:
            num_cycles: Number of review cycles.
            demand_rds: Fixed demand digits (``num_cycles * N`` of them) or
                ``None`` to draw them from ``rng``.
            lead_time_rds: Fixed lead-time digits, one per review (an order is
                placed at the end of each cycle except the last one).
            rng: Object with ``next_digit()`` (e.g. the project's LCG) or a
                ``random.Random``; used when digits are not fixed.
        """
        total = num_cycles * self.N
        if demand_rds is not None and len(demand_rds) < total:
            raise ValueError(f"need {total} demand digits, got {len(demand_rds)}")
        lt_index = 0
        for i in range(total):
            d_rd = demand_rds[i] if demand_rds is not None else _digit(rng, 100)
            self.run_day(d_rd)
            is_review = (i + 1) % self.N == 0
            if is_review and (i + 1) < total:
                if lead_time_rds is not None:
                    l_rd = lead_time_rds[lt_index]
                else:
                    l_rd = _digit(rng, 10)
                lt_index += 1
                self.place_order(l_rd)
        return self.history

    def get_metrics(self) -> Dict[str, float]:
        """Totals: ending inventory, average, shortage days, service level."""
        from module3_inventory.performance import compute_metrics
        return compute_metrics(self.history)


def _digit(rng: Any, base: int) -> Optional[int]:
    """Draw a digit in ``range(base)`` from ``rng`` (None -> table default)."""
    if rng is None:
        return None
    if hasattr(rng, "next_digit"):
        d = rng.next_digit()          # 0-99
        return d % base if base != 100 else d
    return rng.randint(0, base - 1)
