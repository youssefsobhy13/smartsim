"""Sensitivity of the best order quantity to the Good/Fair/Poor probabilities."""

from typing import Dict, List, Optional, Sequence, Tuple

from config.constants import NEWSDAY_TABLE, ORDER_QUANTITIES
from module4_newspaper.optimal_q import analytic_expected_profit

DEFAULT_SCENARIOS: Dict[str, Tuple[float, float, float]] = {
    "baseline (35/45/20)": (0.35, 0.45, 0.20),
    "more good days (60/30/10)": (0.60, 0.30, 0.10),
    "more poor days (10/30/60)": (0.10, 0.30, 0.60),
    "equal (33/34/33)": (0.33, 0.34, 0.33),
}


def probability_sensitivity(scenarios: Optional[Dict[str, Tuple[float, float, float]]] = None,
                            quantities: Sequence[int] = tuple(ORDER_QUANTITIES)
                            ) -> List[Dict[str, object]]:
    """Expected profit per Q and the best Q for each probability scenario.

    Args:
        scenarios: ``{name: (p_good, p_fair, p_poor)}``; must sum to 1.
        quantities: Order quantities to compare.
    """
    scenarios = scenarios or DEFAULT_SCENARIOS
    rows = []
    for name, probs in scenarios.items():
        if abs(sum(probs) - 1.0) > 1e-9:
            raise ValueError(f"probabilities in {name!r} must sum to 1")
        table = [(n, pr, dem, lo, hi)
                 for (n, _p, dem, lo, hi), pr in zip(NEWSDAY_TABLE, probs)]
        profits = {q: analytic_expected_profit(q, table) for q in quantities}
        best = max(profits, key=profits.get)
        rows.append({"scenario": name, "profits": profits, "best_q": best})
    return rows
