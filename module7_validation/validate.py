"""Validation: compare computed results with the lecture (source) values.

The report is HONEST: when a computed value differs from the source it is
shown as ``DIFF`` with the real difference, never silently passed.
"""

from typing import Any, Dict, List

from config.constants import SOURCE_VALUES
from config.settings import REPORTS_DIR, ensure_output_dirs
from module1_probability.continuous_dist import exponential_rv
from module3_inventory.simulation import run_full_simulation
from module4_newspaper.optimal_q import analytic_expected_profit, test_order_quantities

Row = Dict[str, Any]


def _row(metric: str, source: float, computed: float, tol: float,
         note: str = "") -> Row:
    diff = computed - source
    return {"metric": metric, "source": source, "computed": computed,
            "diff": diff, "match": abs(diff) <= tol, "note": note}


def validate_inventory_results(mode: str = "lecture") -> List[Row]:
    """Avg inventory, total ending inventory, shortage days, service level.

    Args:
        mode: ``"lecture"`` (replay of the transcribed table) or ``"rules"``
            (model run with the fixed RDs).
    """
    m = run_full_simulation(mode)["metrics"]
    tag = f"[{mode}]"
    return [
        _row(f"Total ending inventory {tag}", SOURCE_VALUES["total_ending_inventory"],
             m["total_ending_inventory"], 0),
        _row(f"Avg inventory {tag}", SOURCE_VALUES["avg_inventory"],
             m["average_inventory"], 0.05),
        _row(f"Shortage days {tag}", SOURCE_VALUES["shortage_days"],
             m["shortage_days"], 0),
        _row(f"Service level {tag}", SOURCE_VALUES["service_level"],
             m["service_level"], 1e-9),
    ]


def validate_newspaper_results() -> List[Row]:
    """Profit for Q = 40, 50, 60 from the plan's 10-day simulation."""
    sim = test_order_quantities()
    notes = {40: "", 50: "plan RD table gives 6.50; lecture quotes 6.55",
             60: "plan RD table gives 4.20; lecture quotes 4.18"}
    rows = []
    for q in (40, 50, 60):
        rows.append(_row(f"Newspaper (Q={q})", SOURCE_VALUES[f"newspaper_{q}"],
                         round(sim[q], 4), 0.005, notes[q]))
    return rows


def validate_distribution_results() -> List[Row]:
    """Exponential probabilities (pages 43-45)."""
    exp = exponential_rv(1.0)
    return [
        _row("P(X<1) Exp", SOURCE_VALUES["exp_p_lt_1"], exp.cdf(1.0), 1e-6),
        _row("P(1<=X<2.5) Exp", SOURCE_VALUES["exp_p_1_to_2_5"],
             exp.probability(1.0, 2.5), 1e-6),
        _row("P(X>=3) Exp", SOURCE_VALUES["exp_p_ge_3"], 1.0 - exp.cdf(3.0), 1e-6),
    ]


def newspaper_analytic_table() -> List[Row]:
    """Exact expected profits (reference, not a source comparison)."""
    return [{"Q": q, "expected_profit": analytic_expected_profit(q)}
            for q in (40, 50, 60)]


def compare_with_source(save: bool = True, verbose: bool = True) -> Dict[str, Any]:
    """Build, print and (optionally) save the validation table.

    Returns:
        Dict with ``rows``, ``matched``, ``total`` and ``report_path``.
    """
    rows = (validate_inventory_results("lecture") + validate_inventory_results("rules")
            + validate_newspaper_results() + validate_distribution_results())
    lines = [f"{'Metric':<34}{'Source':>10}{'Computed':>11}{'Diff':>10}  Match",
             "-" * 72]
    for r in rows:
        mark = "OK" if r["match"] else "DIFF"
        lines.append(f"{r['metric']:<34}{r['source']:>10.4f}{r['computed']:>11.4f}"
                     f"{r['diff']:>+10.4f}  {mark}" + (f"  ({r['note']})" if r["note"] else ""))
    matched = sum(1 for r in rows if r["match"])
    lines.append("-" * 72)
    lines.append(f"{matched}/{len(rows)} values match the source exactly (within tolerance).")
    lines.append("")
    lines.append("Reference - exact expected newspaper profit: "
                 + ", ".join(f"Q={t['Q']}: {t['expected_profit']:.2f}"
                             for t in newspaper_analytic_table()))
    text = "\n".join(lines)
    path = ""
    if save:
        ensure_output_dirs()
        path = str(REPORTS_DIR / "validation_report.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# SmartSim validation report\n\n```\n" + text + "\n```\n\n"
                     "See README 'Known source discrepancies' for why DIFF rows exist.\n")
    if verbose:
        print(text)
    return {"rows": rows, "matched": matched, "total": len(rows), "report_path": path}
