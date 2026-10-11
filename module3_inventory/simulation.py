"""Full 25-day (M,N) simulation: rule-based run and lecture-table replay.

Two modes are provided because the lecture table (as transcribed in the
SmartSim plan) cannot be reproduced from the lecture's own rules:

* ``"rules"``  - run the model with the fixed demand RDs (honest computation).
* ``"lecture"`` - replay the transcribed table row by row, typos included.

See README section "Known source discrepancies".
"""

from typing import Any, Dict, List, Tuple

from config.constants import (FIXED_DEMAND_RDS, INITIAL_INVENTORY,
                              LECTURE_LEAD_TIME_RDS, M_MAX, N_REVIEW,
                              NUM_CYCLES, PENDING_ARRIVAL_DAY, PENDING_UNITS)
from module3_inventory.inventory_system import InventorySystemMN
from module3_inventory.performance import compute_metrics

# (cycle, day, begin, rd, demand, end, shortage_units, note)  as transcribed
LECTURE_TABLE: List[Tuple[int, int, int, int, int, int, int, str]] = [
    (1, 1, 3, 24, 1, 2, 0, "Order due"),
    (1, 2, 10, 35, 1, 9, 0, "Arrived"),
    (1, 3, 9, 65, 2, 7, 0, ""),
    (1, 4, 7, 81, 3, 4, 0, ""),
    (1, 5, 4, 54, 2, 2, 0, "Order 9, LT 1"),
    (2, 1, 11, 3, 0, 11, 0, "Arrived"),
    (2, 2, 11, 87, 3, 8, 0, ""),
    (2, 3, 8, 27, 1, 7, 0, ""),
    (2, 4, 7, 47, 2, 5, 0, ""),
    (2, 5, 5, 70, 2, 2, 0, "Order 9, LT 3"),   # begin 5 - demand 2 = 3, table says 2
    (3, 1, 2, 30, 2, 0, 0, ""),                 # RD 30 maps to demand 1, table says 2
    (3, 2, 0, 30, 2, 0, 2, "Shortage 2"),
    (3, 3, 0, 30, 2, 0, 2, "Shortage 4"),
    (3, 4, 5, 17, 1, 4, 0, "Arrived"),
    (3, 5, 4, 9, 0, 4, 0, "Order 7, LT 1"),
    (4, 1, 11, 42, 2, 9, 0, "Arrived"),
    (4, 2, 9, 87, 3, 6, 0, ""),
    (4, 3, 6, 26, 1, 5, 0, ""),
    (4, 4, 5, 36, 2, 3, 0, ""),
    (4, 5, 3, 40, 2, 1, 0, "Order 10, LT 1"),
    (5, 1, 11, 3, 0, 11, 0, "Arrived"),
    (5, 2, 11, 63, 2, 9, 0, ""),
    (5, 3, 9, 19, 1, 8, 0, ""),
    (5, 4, 8, 88, 3, 5, 0, ""),
    (5, 5, 5, 94, 4, 1, 0, ""),
]


def lecture_history() -> List[Dict[str, Any]]:
    """The transcribed lecture table in the standard history format."""
    rows = []
    for i, (cyc, day, begin, rd, dem, end, short, note) in enumerate(LECTURE_TABLE, 1):
        rows.append({"cycle": cyc, "day": day, "abs_day": i, "begin": begin,
                     "rd_demand": rd, "demand": dem, "end": end,
                     "shortage": short, "order_qty": None, "lead_time": None,
                     "note": note})
    return rows


def rules_history() -> List[Dict[str, Any]]:
    """Run the (M,N) model with the fixed demand RDs and lecture lead times."""
    system = InventorySystemMN(M_MAX, N_REVIEW, INITIAL_INVENTORY,
                               (PENDING_UNITS, PENDING_ARRIVAL_DAY))
    return system.run_cycles(NUM_CYCLES, FIXED_DEMAND_RDS, LECTURE_LEAD_TIME_RDS)


def format_table(history: List[Dict[str, Any]]) -> str:
    """Plain-text table of a history."""
    lines = [f"{'Cyc':>3} {'Day':>3} {'Begin':>5} {'RD':>3} {'Dem':>3} "
             f"{'End':>3} {'Short':>5}  Notes",
             "-" * 52]
    for r in history:
        rd = "-" if r["rd_demand"] is None else f"{r['rd_demand']:02d}"
        lines.append(f"{r['cycle']:>3} {r['day']:>3} {r['begin']:>5} {rd:>3} "
                     f"{r['demand']:>3} {r['end']:>3} {r['shortage']:>5}  {r['note']}")
    return "\n".join(lines)


def run_full_simulation(mode: str = "rules", verbose: bool = False) -> Dict[str, Any]:
    """Run the 5-cycle example.

    Args:
        mode: ``"rules"`` (model run) or ``"lecture"`` (transcribed table).
        verbose: Print the table and metrics.

    Returns:
        Dict with ``history`` and ``metrics``.
    """
    if mode == "rules":
        history = rules_history()
    elif mode == "lecture":
        history = lecture_history()
    else:
        raise ValueError("mode must be 'rules' or 'lecture'")
    metrics = compute_metrics(history)
    if verbose:
        print(format_table(history))
        print(f"\nTotal ending inventory: {metrics['total_ending_inventory']}")
        print(f"Average inventory     : {metrics['average_inventory']:.2f}")
        print(f"Shortage days         : {metrics['shortage_days']}")
        print(f"Service level         : {metrics['service_level']:.0%}")
    return {"history": history, "metrics": metrics, "mode": mode}
