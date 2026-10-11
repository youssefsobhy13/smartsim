"""General settings (paths, defaults)."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
PLOTS_DIR = RESULTS_DIR / "plots"
REPORTS_DIR = RESULTS_DIR / "reports"

DEFAULT_SEED = 2025
DEFAULT_REPLICATIONS = 30
DEFAULT_CONFIDENCE = 0.95
FLOAT_TOLERANCE = 1e-6


def ensure_output_dirs() -> None:
    """Create results/plots and results/reports if they do not exist."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
