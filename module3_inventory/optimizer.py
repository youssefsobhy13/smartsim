"""Optimal (M,N) search and sensitivity analysis.

Cost rates are ASSUMED (see ``config/constants.py``); the plan gives none.
"""

from statistics import mean
from typing import Dict, List, Optional, Sequence, Tuple

from config.constants import (HOLDING_COST_PER_UNIT_DAY,
                              ORDERING_COST_PER_ORDER, SHORTAGE_COST_PER_UNIT)
from module2_random.lcg import LinearCongruentialGenerator
from module3_inventory.inventory_system import InventorySystemMN
from module3_inventory.performance import compute_metrics, total_cost

SIM_DAYS = 60


def _replicate(M: int, N: int, replications: int, seed: int,
               costs: Optional[Dict[str, float]] = None,
               demand_shift: int = 0, lead_shift: int = 0
               ) -> Tuple[float, Dict[str, float]]:
    """Average cost and metrics over replications with seeds seed, seed+1, ..."""
    cycles = max(1, SIM_DAYS // N)
    costs_l: List[float] = []
    metrics_l: List[Dict[str, float]] = []
    for rep in range(replications):
        rng = LinearCongruentialGenerator(seed=seed + rep)
        system = InventorySystemMN(M, N, initial=M, pending=None,
                                   demand_shift=demand_shift, lead_shift=lead_shift)
        system.run_cycles(cycles, rng=rng)
        costs_l.append(total_cost(system.history, costs) / len(system.history))
        metrics_l.append(compute_metrics(system.history))
    avg_metrics = {k: mean(m[k] for m in metrics_l) for k in metrics_l[0]}
    return mean(costs_l), avg_metrics


def cost_function(M: int, N: int, replications: int = 30, seed: int = 2025,
                  costs: Optional[Dict[str, float]] = None) -> float:
    """Average total cost per day for one (M,N) pair."""
    return _replicate(M, N, replications, seed, costs)[0]


def find_optimal_M_N(M_values: Sequence[int] = tuple(range(6, 21)),
                     N_values: Sequence[int] = (3, 4, 5, 6, 7),
                     replications: int = 30, seed: int = 2025,
                     costs: Optional[Dict[str, float]] = None) -> Dict[str, object]:
    """Grid search for the (M,N) with minimum average daily cost.

    All pairs use the same seeds (common random numbers), and the (11,5)
    baseline is always evaluated so the optimum is never worse than it.

    Returns:
        Dict with ``best`` ``(M, N)``, ``best_cost``, ``baseline_cost`` and the
        full ``table`` (list of dicts).
    """
    pairs = {(M, N) for M in M_values for N in N_values} | {(11, 5)}
    table = [{"M": M, "N": N, "cost": cost_function(M, N, replications, seed, costs)}
             for M, N in sorted(pairs)]
    best = min(table, key=lambda r: r["cost"])
    base = next(r for r in table if (r["M"], r["N"]) == (11, 5))
    return {"best": (best["M"], best["N"]), "best_cost": best["cost"],
            "baseline_cost": base["cost"], "table": table}


def sensitivity_analysis(M: int = 11, N: int = 5, replications: int = 30,
                         seed: int = 2025) -> List[Dict[str, object]]:
    """Vary demand, lead time and cost rates; return a table of results."""
    base_costs = {"holding": HOLDING_COST_PER_UNIT_DAY,
                  "ordering": ORDERING_COST_PER_ORDER,
                  "shortage": SHORTAGE_COST_PER_UNIT}
    scenarios = [
        ("baseline", {}, 0, 0),
        ("demand +1", {}, 1, 0), ("demand -1", {}, -1, 0),
        ("lead time +1", {}, 0, 1),
        ("holding cost x2", {"holding": base_costs["holding"] * 2}, 0, 0),
        ("ordering cost x2", {"ordering": base_costs["ordering"] * 2}, 0, 0),
        ("shortage cost x2", {"shortage": base_costs["shortage"] * 2}, 0, 0),
    ]
    rows = []
    for name, costs, dshift, lshift in scenarios:
        cost, m = _replicate(M, N, replications, seed, costs, dshift, lshift)
        rows.append({"scenario": name, "avg_daily_cost": cost,
                     "avg_inventory": m["average_inventory"],
                     "service_level": m["service_level"]})
    return rows
