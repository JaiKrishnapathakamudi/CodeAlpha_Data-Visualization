"""
Chart 01 — Global Temperature Anomaly (1950–2024)
Type: Annotated area chart with trend line
Story: Climate change made visceral through rising temperature anomalies.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.signal import savgol_filter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, OUTPUT_DIR


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    # ── Data ──────────────────────────────────────────────────────────────────
    rng = np.random.default_rng(42)
    years = np.arange(1950, 2025)
    trend = (years - 1950) * 0.018
    noise = rng.normal(0, 0.12, len(years))
    anomaly = trend + noise
    df = pd.DataFrame({"year": years, "anomaly": anomaly})
    smooth = savgol_filter(anomaly, window_length=9, polyorder=2)

    # ── Figure ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.subplots_adjust(left=0.08, right=0.96, top=0.88, bottom=0.12)

    # Zero baseline
    ax.axhline(0, color=PALETTE["muted"], linewidth=0.8, linestyle="--", alpha=0.5)

    # Fill above/below baseline
    ax.fill_between(years, anomaly, 0,
                    where=(anomaly >= 0), interpolate=True,
                    color=PALETTE["danger"], alpha=0.25, label="_nolegend_")
    ax.fill_between(years, anomaly, 0,
                    where=(anomaly < 0), interpolate=True,
                    color=PALETTE["accent"], alpha=0.25, label="_nolegend_")

    # Raw values (scatter)
    colors = [PALETTE["danger"] if v >= 0 else PALETTE["accent"] for v in anomaly]
    ax.scatter(years, anomaly, c=colors, s=22, zorder=3, alpha=0.7)

    # Smoothed trend
    ax.plot(years, smooth, color=PALETTE["warning"], linewidth=2.5,
            label="10-yr smoothed trend", zorder=4)

    # ── Annotations ───────────────────────────────────────────────────────────
    peak_idx = np.argmax(anomaly)
    ax.annotate(
        f"Peak: +{anomaly[peak_idx]:.2f}°C\n({years[peak_idx]})",
        xy=(years[peak_idx], anomaly[peak_idx]),
        xytext=(years[peak_idx] - 10, anomaly[peak_idx] + 0.15),
        fontsize=9, color=PALETTE["text"],
        arrowprops=dict(arrowstyle="->", color=PALETTE["muted"], lw=1.2),
        bbox=dict(boxstyle="round,pad=0.3", fc=PALETTE["surface"], ec=PALETTE["border"], lw=0.8),
    )
    ax.annotate("Pre-industrial\nbaseline (0°C)", xy=(1952, 0.02),
                fontsize=8, color=PALETTE["muted"])

    # ── Cosmetics ─────────────────────────────────────────────────────────────
    ax.set_title("Global Temperature Anomaly  ·  1950 – 2024",
                 fontsize=15, fontweight="bold", color=PALETTE["text"], pad=14)
    ax.set_xlabel("Year", labelpad=8)
    ax.set_ylabel("Anomaly (°C)", labelpad=8)
    ax.set_xlim(1948, 2026)

    warm_patch = mpatches.Patch(color=PALETTE["danger"], alpha=0.5, label="Warmer than baseline")
    cool_patch = mpatches.Patch(color=PALETTE["accent"], alpha=0.5, label="Cooler than baseline")
    trend_line = plt.Line2D([0], [0], color=PALETTE["warning"], lw=2.5, label="Smoothed trend")
    ax.legend(handles=[warm_patch, cool_patch, trend_line],
              loc="upper left", framealpha=0.9)

    add_watermark(fig)
    if save:
        fig.savefig(OUTPUT_DIR / "01_climate_anomaly.png", bbox_inches="tight")
        print("  ✓ 01_climate_anomaly.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
