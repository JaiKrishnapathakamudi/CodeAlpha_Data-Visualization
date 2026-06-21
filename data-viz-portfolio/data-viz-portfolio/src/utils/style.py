"""
Shared style configuration for all visualizations.
Ensures a consistent visual identity across the portfolio.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# ── Palette ────────────────────────────────────────────────────────────────────
PALETTE = {
    "bg":        "#0D1117",   # deep navy — canvas
    "surface":   "#161B22",   # card surface
    "border":    "#21262D",   # subtle dividers
    "text":      "#E6EDF3",   # primary text
    "muted":     "#8B949E",   # secondary text
    "accent":    "#58A6FF",   # electric blue — primary accent
    "accent2":   "#3FB950",   # mint green — secondary
    "accent3":   "#F78166",   # coral — tertiary
    "accent4":   "#D2A8FF",   # lavender — quaternary
    "accent5":   "#FFA657",   # amber — quinary
    "warning":   "#F0883E",
    "danger":    "#F85149",
}

SEQUENTIAL = ["#0D1117", "#0C2A4A", "#0E4080", "#1565C0", "#1976D2",
               "#2196F3", "#42A5F5", "#64B5F6", "#90CAF9", "#BBDEFB"]

CATEGORICAL = [
    PALETTE["accent"],  PALETTE["accent2"], PALETTE["accent3"],
    PALETTE["accent4"], PALETTE["accent5"], "#79C0FF", "#56D364",
]

DIVERGING = ["#F85149", "#FF7B72", "#FFA657", "#E6EDF3", "#58A6FF", "#1F6FEB", "#0D419D"]


# ── Rcparams ───────────────────────────────────────────────────────────────────
def apply_theme() -> None:
    """Apply the portfolio dark theme globally to Matplotlib."""
    mpl.rcParams.update({
        # Canvas
        "figure.facecolor":     PALETTE["bg"],
        "axes.facecolor":       PALETTE["surface"],
        "savefig.facecolor":    PALETTE["bg"],
        "savefig.edgecolor":    "none",
        # Grid & spines
        "axes.edgecolor":       PALETTE["border"],
        "axes.grid":            True,
        "grid.color":           PALETTE["border"],
        "grid.linewidth":       0.6,
        "grid.alpha":           0.7,
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        # Text
        "text.color":           PALETTE["text"],
        "axes.labelcolor":      PALETTE["muted"],
        "xtick.color":          PALETTE["muted"],
        "ytick.color":          PALETTE["muted"],
        "axes.titlecolor":      PALETTE["text"],
        "axes.titlesize":       14,
        "axes.titleweight":     "bold",
        "axes.labelsize":       11,
        "xtick.labelsize":      10,
        "ytick.labelsize":      10,
        # Font
        "font.family":          "sans-serif",
        "font.sans-serif":      ["DejaVu Sans", "Liberation Sans", "Helvetica Neue", "Arial", "sans-serif"],
        # Legend
        "legend.facecolor":     PALETTE["surface"],
        "legend.edgecolor":     PALETTE["border"],
        "legend.labelcolor":    PALETTE["text"],
        "legend.fontsize":      10,
        # Lines
        "lines.linewidth":      2.0,
        "lines.antialiased":    True,
        # Figure
        "figure.dpi":           150,
        "savefig.dpi":          180,
        "figure.autolayout":    False,
    })


def add_watermark(fig: plt.Figure, text: str = "Data Viz Portfolio") -> None:
    fig.text(0.99, 0.01, text, ha="right", va="bottom",
             fontsize=8, color=PALETTE["muted"], alpha=0.5,
             fontstyle="italic")


OUTPUT_DIR = Path(__file__).parent / "../../assets/images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
