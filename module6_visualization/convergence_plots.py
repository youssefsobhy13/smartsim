"""Convergence plots: LLN and CLT (page 57)."""

from typing import Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from module6_visualization._common import save_figure


def plot_lln(running_mean: Sequence[float], true_mean: float = 1.0,
             save_path: Optional[str] = None) -> str:
    """Running sample mean vs n, with the true mean as a dashed line."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(np.arange(1, len(running_mean) + 1), running_mean, color="#2b8cbe",
            label="Sample mean")
    ax.axhline(true_mean, color="green", linestyle="--", label=f"mean = {true_mean:g}")
    ax.set_xlabel("Sample size n")
    ax.set_ylabel("Running mean")
    ax.set_title("Law of large numbers")
    ax.legend()
    return save_figure(fig, "lln_convergence.png", save_path)


def plot_clt(standardised_sums: Sequence[float], bins: int = 40,
             save_path: Optional[str] = None) -> str:
    """Histogram of standardised sums with the standard normal density."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(standardised_sums, bins=bins, density=True, color="#9ecae1",
            edgecolor="white", label="Standardised sums")
    x = np.linspace(-4, 4, 400)
    ax.plot(x, stats.norm.pdf(x), color="red", label="N(0, 1)")
    ax.set_title("Central limit theorem")
    ax.set_xlabel("z")
    ax.set_ylabel("Density")
    ax.legend()
    return save_figure(fig, "clt_histogram.png", save_path)
