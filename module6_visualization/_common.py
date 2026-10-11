"""Shared helpers for the plotting modules (headless matplotlib backend)."""

from pathlib import Path
from typing import Optional

import matplotlib

matplotlib.use("Agg")  # no GUI needed; works on servers and in tests
import matplotlib.pyplot as plt  # noqa: E402

from config.settings import PLOTS_DIR, ensure_output_dirs  # noqa: E402


def output_path(filename: str, save_path: Optional[str] = None) -> Path:
    """Where a plot is written: ``save_path`` or ``results/plots/<filename>``."""
    if save_path:
        path = Path(save_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    ensure_output_dirs()
    return PLOTS_DIR / filename


def save_figure(fig, filename: str, save_path: Optional[str] = None) -> str:
    """Save ``fig`` as PNG, close it and return the file path."""
    path = output_path(filename, save_path)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return str(path)
