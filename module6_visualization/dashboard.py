"""Interactive dashboard (Plotly) with a static HTML fallback.

If Plotly is installed the dashboard is interactive. If it is not, a static
HTML page with embedded matplotlib images is written instead so the menu
option still works (``pip install plotly`` enables the interactive version).
"""

import base64
import io
from typing import Dict, List, Optional

from config.settings import REPORTS_DIR, ensure_output_dirs

History = List[Dict]


def plotly_available() -> bool:
    """True if the plotly package can be imported."""
    try:
        import plotly  # noqa: F401
        return True
    except ImportError:
        return False


def create_dashboard(history: History, M: int = 11, save_path: Optional[str] = None,
                     force_static: bool = False) -> str:
    """Create the dashboard: inventory chart, demand histogram, shortage analysis.

    Returns:
        Path of the HTML file (``results/reports/dashboard.html`` by default).
    """
    ensure_output_dirs()
    path = save_path or str(REPORTS_DIR / "dashboard.html")
    if plotly_available() and not force_static:
        _plotly_dashboard(history, M, path)
    else:
        _static_dashboard(history, M, path)
    return path


def _plotly_dashboard(history: History, M: int, path: str) -> None:
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    days = [r["abs_day"] for r in history]
    fig = make_subplots(rows=3, cols=1, subplot_titles=(
        "Inventory over time", "Demand histogram", "Shortage analysis"))
    fig.add_trace(go.Scatter(x=days, y=[r["end"] for r in history],
                             mode="lines+markers", name="Ending inventory"), 1, 1)
    fig.add_hline(y=M, line_dash="dash", annotation_text=f"M = {M}", row=1, col=1)
    short = [r for r in history if r["shortage"] > 0]
    fig.add_trace(go.Scatter(x=[r["abs_day"] for r in short],
                             y=[r["end"] for r in short], mode="markers",
                             marker=dict(color="red", size=12), name="Shortage"), 1, 1)
    fig.add_trace(go.Histogram(x=[r["demand"] for r in history], name="Demand"), 2, 1)
    fig.add_trace(go.Bar(x=days, y=[r["shortage"] for r in history],
                         name="Unserved units"), 3, 1)
    fig.update_layout(height=900, title="SmartSim - Inventory dashboard")
    fig.write_html(path, include_plotlyjs="cdn")


def _png_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _static_dashboard(history: History, M: int, path: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    days = [r["abs_day"] for r in history]
    images = []

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(days, [r["end"] for r in history], marker="o")
    ax.axhline(M, linestyle="--", color="orange")
    ax.set_title("Inventory over time")
    images.append(_png_base64(fig)); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.hist([r["demand"] for r in history], bins=range(0, 7), align="left")
    ax.set_title("Demand histogram")
    images.append(_png_base64(fig)); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.bar(days, [r["shortage"] for r in history], color="red")
    ax.set_title("Shortage analysis")
    images.append(_png_base64(fig)); plt.close(fig)

    body = "".join(f'<img src="data:image/png;base64,{b}" style="max-width:100%"><br>'
                   for b in images)
    html = ("<html><head><meta charset='utf-8'><title>SmartSim dashboard</title></head>"
            "<body style='font-family:sans-serif;max-width:960px;margin:auto'>"
            "<h1>SmartSim - Inventory dashboard</h1>"
            "<p><i>Static version (install plotly for the interactive one).</i></p>"
            f"{body}</body></html>")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
