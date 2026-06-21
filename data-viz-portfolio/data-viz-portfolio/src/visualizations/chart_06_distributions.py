"""
Chart 06 — Revenue Distribution Analysis
Type: Violin + strip plot + box summary (Seaborn showcase)
Story: Compare revenue distributions across product categories with statistical depth.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, CATEGORICAL, OUTPUT_DIR


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    rng = np.random.default_rng(42)
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    records = []
    for i, cat in enumerate(categories):
        base = [80, 35, 55, 45, 20][i] * 1000
        n    = rng.integers(180, 220)
        vals = rng.gamma(shape=2.5, scale=base / 2.5, size=n)
        # add a few outliers
        vals = np.append(vals, rng.uniform(base * 2, base * 3.5, size=rng.integers(3, 8)))
        for v in vals:
            records.append({"Category": cat, "Revenue_USD": v})
    df = pd.DataFrame(records)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7),
                             gridspec_kw={"width_ratios": [3, 2]})
    fig.subplots_adjust(left=0.08, right=0.97, top=0.88, bottom=0.12, wspace=0.3)

    # ── Violin + strip ─────────────────────────────────────────────────────────
    ax = axes[0]
    sns.violinplot(data=df, x="Category", y="Revenue_USD", ax=ax,
                   hue="Category", palette=CATEGORICAL[:5],
                   inner=None, alpha=0.7, linewidth=1.2, legend=False)
    sns.stripplot(data=df, x="Category", y="Revenue_USD", ax=ax,
                  color=PALETTE["text"], size=2.5, alpha=0.35, jitter=True)
    ax.set_title("Revenue Distribution by Category\n(violin + individual transactions)",
                 fontsize=12, fontweight="bold", color=PALETTE["text"])
    ax.set_xlabel("")
    ax.set_ylabel("Revenue per Order (USD)", labelpad=8)
    ax.tick_params(axis="x", labelsize=9)

    # ── Horizontal box summary ─────────────────────────────────────────────────
    ax2 = axes[1]
    summary = df.groupby("Category")["Revenue_USD"].describe()[["25%", "50%", "75%", "mean"]]
    summary = summary.sort_values("mean", ascending=True)
    colors_map = dict(zip(categories, CATEGORICAL[:5]))

    for i, (cat, row) in enumerate(summary.iterrows()):
        c = colors_map[cat]
        # IQR bar
        ax2.barh(i, row["75%"] - row["25%"], left=row["25%"],
                 height=0.45, color=c, alpha=0.5)
        # Median line
        ax2.vlines(row["50%"], i - 0.25, i + 0.25, color=c, linewidth=2.5)
        # Mean diamond
        ax2.scatter(row["mean"], i, marker="D", color=PALETTE["warning"],
                    s=55, zorder=5)
        ax2.text(row["75%"] + 500, i, f"${row['mean']/1000:.1f}k", va="center",
                 fontsize=8.5, color=PALETTE["muted"])

    ax2.set_yticks(range(len(summary)))
    ax2.set_yticklabels(summary.index, fontsize=9)
    ax2.set_xlabel("Revenue (USD)", labelpad=8)
    ax2.set_title("IQR Summary  ·  ◆ = Mean",
                  fontsize=12, fontweight="bold", color=PALETTE["text"])

    fig.suptitle("Transaction Revenue Distribution Analysis",
                 fontsize=15, fontweight="bold", color=PALETTE["text"])
    add_watermark(fig)

    if save:
        fig.savefig(OUTPUT_DIR / "06_distributions.png", bbox_inches="tight")
        print("  ✓ 06_distributions.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
