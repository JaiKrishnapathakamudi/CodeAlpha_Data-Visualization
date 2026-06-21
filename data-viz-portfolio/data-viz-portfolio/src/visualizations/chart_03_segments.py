"""
Chart 03 — Customer RFM Segmentation
Type: Bubble scatter (Recency × Frequency, bubble = Monetary)
Story: Show where customers cluster and which segments drive revenue.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, CATEGORICAL, OUTPUT_DIR


SEGMENT_COLORS = {
    "Champions": CATEGORICAL[1],   # mint
    "Loyal":     CATEGORICAL[0],   # blue
    "At Risk":   CATEGORICAL[4],   # amber
    "Lost":      CATEGORICAL[2],   # coral
    "New":       CATEGORICAL[3],   # lavender
}


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    rng = np.random.default_rng(42)
    n = 800
    segments = {
        "Champions": (0.15, (1,10),   (20,50),  (5000,20000)),
        "Loyal":     (0.20, (10,30),  (10,25),  (2000,8000)),
        "At Risk":   (0.25, (60,120), (5,15),   (500,3000)),
        "Lost":      (0.25, (150,365),(1,5),    (50,500)),
        "New":       (0.15, (1,30),   (1,3),    (100,1000)),
    }
    records = []
    for seg, (frac, rec, freq, mon) in segments.items():
        k = int(n * frac)
        records.extend([{
            "segment": seg,
            "recency": rng.integers(*rec),
            "frequency": rng.integers(*freq),
            "monetary": rng.uniform(*mon),
        } for _ in range(k)])
    df = pd.DataFrame(records)

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.88, bottom=0.12)

    for seg, grp in df.groupby("segment"):
        sizes = (grp["monetary"] / grp["monetary"].max()) * 300 + 20
        ax.scatter(grp["recency"], grp["frequency"],
                   s=sizes, c=SEGMENT_COLORS[seg], alpha=0.6,
                   edgecolors=PALETTE["bg"], linewidths=0.4, label=seg)

    # Quadrant lines
    med_rec  = df["recency"].median()
    med_freq = df["frequency"].median()
    ax.axvline(med_rec,  color=PALETTE["border"], linewidth=1, linestyle="--", alpha=0.8)
    ax.axhline(med_freq, color=PALETTE["border"], linewidth=1, linestyle="--", alpha=0.8)

    # Quadrant labels
    for (x, y, label) in [
        (0.02, 0.97, "High Freq\nRecent"), (0.55, 0.97, "High Freq\nLapsed"),
        (0.02, 0.05, "Low Freq\nRecent"), (0.55, 0.05, "Low Freq\nLapsed"),
    ]:
        ax.text(x, y, label, transform=ax.transAxes, fontsize=8,
                color=PALETTE["muted"], va="top" if y > 0.5 else "bottom", alpha=0.8)

    ax.set_title("Customer Segmentation  ·  RFM Analysis\n"
                 "Bubble size = Lifetime Value (USD)",
                 fontsize=13, fontweight="bold", color=PALETTE["text"])
    ax.set_xlabel("Recency (days since last purchase)  ←  More recent", labelpad=8)
    ax.set_ylabel("Purchase Frequency", labelpad=8)
    ax.invert_xaxis()

    # Size legend
    for val, label in [(500, "$500"), (5000, "$5 k"), (15000, "$15 k")]:
        ax.scatter([], [], s=(val / df["monetary"].max()) * 300 + 20,
                   c=PALETTE["muted"], alpha=0.5, label=f"LTV {label}")

    ax.legend(ncol=2, loc="upper right", framealpha=0.9, fontsize=9)
    add_watermark(fig)

    if save:
        fig.savefig(OUTPUT_DIR / "03_customer_segments.png", bbox_inches="tight")
        print("  ✓ 03_customer_segments.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
