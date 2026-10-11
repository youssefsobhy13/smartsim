"""Distribution plots: PMF/CDF, histograms, comparisons (pages 32-34)."""

from typing import Callable, Dict, Optional, Sequence

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from module1_probability.discrete_dist import DiscreteDistribution
from module6_visualization._common import save_figure


def plot_pmf_cdf(dist: DiscreteDistribution, save_path: Optional[str] = None) -> str:
    """Left: PMF bars. Right: CDF step function. Title = distribution name."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    ax1.bar(dist.values, dist.probabilities, color="#2b8cbe")
    ax1.set_title(f"{dist.name} - PMF")
    ax1.set_xlabel("x")
    ax1.set_ylabel("P(X = x)")
    xs = list(dist.values)
    cdf = [dist.cdf(x) for x in xs]
    ax2.step([xs[0] - 1] + xs + [xs[-1] + 1], [0] + cdf + [1], where="post",
             color="#e6a700")
    ax2.set_title(f"{dist.name} - CDF")
    ax2.set_xlabel("x")
    ax2.set_ylabel("P(X <= x)")
    ax2.set_ylim(0, 1.05)
    fig.suptitle(dist.name)
    return save_figure(fig, "pmf_cdf.png", save_path)


def plot_histogram(data: Sequence[float], bins: int = 20, title: str = "Histogram",
                   save_path: Optional[str] = None) -> str:
    """Histogram of a data sample."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data, bins=bins, color="#31a354", edgecolor="white")
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    return save_figure(fig, "histogram.png", save_path)


def plot_comparison(pdfs: Optional[Dict[str, Callable[[np.ndarray], np.ndarray]]] = None,
                    x_range=(-4.0, 8.0), save_path: Optional[str] = None) -> str:
    """Several densities on the same axes (default: normal, uniform, skewed)."""
    pdfs = pdfs or {
        "Normal(2, 1)": lambda x: stats.norm.pdf(x, 2, 1),
        "Uniform(0, 4)": lambda x: stats.uniform.pdf(x, 0, 4),
        "Exponential(1) (skewed)": lambda x: stats.expon.pdf(x),
    }
    x = np.linspace(*x_range, 600)
    fig, ax = plt.subplots(figsize=(8, 4))
    for name, f in pdfs.items():
        ax.plot(x, f(x), label=name)
    ax.set_title("Distribution comparison")
    ax.set_xlabel("x")
    ax.set_ylabel("Density")
    ax.legend()
    return save_figure(fig, "distribution_comparison.png", save_path)
