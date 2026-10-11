"""Inventory plots (pages 113-115)."""

from typing import Dict, List, Optional

import matplotlib.pyplot as plt

from module6_visualization._common import save_figure

History = List[Dict]


def plot_inventory_over_time(history: History, M: int = 11, N: int = 5,
                             save_path: Optional[str] = None) -> str:
    """Line plot of ending inventory, days 1-25, with the M line, shortage
    markers and cycle boundaries. Returns the PNG path."""
    days = [r["abs_day"] for r in history]
    levels = [r["end"] for r in history]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(days, levels, marker="o", color="#2b8cbe", label="Ending inventory")
    ax.axhline(M, color="#e6a700", linestyle="--", label=f"M = {M}")
    for boundary in range(N, max(days), N):
        ax.axvline(boundary + 0.5, color="grey", linestyle=":", linewidth=1)
    short = [r for r in history if r["shortage"] > 0]
    if short:
        ax.scatter([r["abs_day"] for r in short], [r["end"] for r in short],
                   color="red", s=90, zorder=5, label="Shortage")
    ax.set_xlim(1, max(days))
    ax.set_ylim(0, max(M, max(levels)) + 1)
    ax.set_xlabel("Day")
    ax.set_ylabel("Units")
    ax.set_title("Inventory over time")
    ax.legend(loc="upper right")
    return save_figure(fig, "inventory_over_time.png", save_path)


def plot_inventory_cycle(history: History, cycle: int,
                         save_path: Optional[str] = None) -> str:
    """Ending inventory and demand for one cycle."""
    rows = [r for r in history if r["cycle"] == cycle]
    if not rows:
        raise ValueError(f"no data for cycle {cycle}")
    fig, ax = plt.subplots(figsize=(6, 4))
    days = [r["day"] for r in rows]
    ax.plot(days, [r["end"] for r in rows], marker="o", label="Ending inventory")
    ax.bar(days, [r["demand"] for r in rows], alpha=0.3, color="#fc8d59",
           label="Demand")
    ax.set_xlabel("Day in cycle")
    ax.set_ylabel("Units")
    ax.set_title(f"Cycle {cycle}")
    ax.legend()
    return save_figure(fig, f"inventory_cycle_{cycle}.png", save_path)


def plot_shortage_analysis(history: History,
                           save_path: Optional[str] = None) -> str:
    """Bar chart of unserved units per day (shortage days highlighted)."""
    days = [r["abs_day"] for r in history]
    units = [r["shortage"] for r in history]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.bar(days, units, color=["red" if u else "#cccccc" for u in units])
    ax.set_xlabel("Day")
    ax.set_ylabel("Unserved units")
    n_days = sum(1 for u in units if u)
    ax.set_title(f"Shortage analysis: {n_days} shortage day(s), {sum(units)} unit(s)")
    return save_figure(fig, "shortage_analysis.png", save_path)
