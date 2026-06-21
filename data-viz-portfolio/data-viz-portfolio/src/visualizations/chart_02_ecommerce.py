"""
Chart 02 — E-Commerce Sales by Category (2022–2024)
Type: Stacked area chart + 12-month rolling YoY bar inset
Story: Reveal seasonal patterns and category growth in online retail.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, CATEGORICAL, OUTPUT_DIR


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    # ── Data ──────────────────────────────────────────────────────────────────
    rng = np.random.default_rng(42)
    months = pd.date_range("2022-01", "2024-12", freq="MS")
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    data = {}
    for cat in categories:
        base = rng.uniform(50_000, 200_000)
        seasonal = np.sin(np.linspace(0, 4 * np.pi, len(months))) * base * 0.2
        trend = np.linspace(0, base * 0.3, len(months))
        noise = rng.normal(0, base * 0.05, len(months))
        data[cat] = (base + seasonal + trend + noise).clip(min=0)

    df = pd.DataFrame(data, index=months)
    total = df.sum(axis=1)
    yoy = ((total / total.shift(12)) - 1).dropna() * 100

    # ── Layout ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 7))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1], figure=fig,
                           left=0.07, right=0.97, top=0.87, bottom=0.12, wspace=0.05)
    ax_main = fig.add_subplot(gs[0])
    ax_bar  = fig.add_subplot(gs[1])

    # ── Stacked area ──────────────────────────────────────────────────────────
    ax_main.stackplot(df.index, [df[c] / 1e6 for c in categories],
                      labels=categories, colors=CATEGORICAL[:5], alpha=0.88)
    ax_main.set_title("Monthly Revenue by Category  (USD, millions)",
                       fontsize=13, fontweight="bold", color=PALETTE["text"])
    ax_main.set_ylabel("Revenue (M USD)", labelpad=8)
    ax_main.set_xlabel("")
    ax_main.legend(loc="upper left", ncol=2, fontsize=9, framealpha=0.85)

    # ── YoY bar ───────────────────────────────────────────────────────────────
    bar_colors = [PALETTE["accent2"] if v >= 0 else PALETTE["danger"] for v in yoy]
    ax_bar.barh(yoy.index, yoy.values, color=bar_colors, alpha=0.85, height=20)
    ax_bar.axvline(0, color=PALETTE["muted"], linewidth=0.8)
    ax_bar.set_title("YoY\nGrowth %", fontsize=10, color=PALETTE["text"])
    ax_bar.set_xlabel("%", labelpad=4)
    ax_bar.yaxis.set_visible(False)
    ax_bar.tick_params(axis="x", labelsize=8)

    fig.suptitle("E-Commerce Performance Dashboard  ·  2022 – 2024",
                 fontsize=15, fontweight="bold", color=PALETTE["text"], y=0.97)
    add_watermark(fig)

    if save:
        fig.savefig(OUTPUT_DIR / "02_ecommerce_sales.png", bbox_inches="tight")
        print("  ✓ 02_ecommerce_sales.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
