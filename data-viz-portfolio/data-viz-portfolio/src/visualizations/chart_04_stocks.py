"""
Chart 04 — Stock Performance Dashboard
Type: Multi-panel (normalized returns + rolling volatility + correlation heatmap)
Story: Compare how tech stocks move together and diverge under stress.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, CATEGORICAL, OUTPUT_DIR


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    # ── Simulate OHLCV ────────────────────────────────────────────────────────
    rng = np.random.default_rng(42)
    tickers = ["ALFA", "BETA", "GAMA", "DELT", "EPSI"]
    dates = pd.bdate_range("2023-01-01", "2024-12-31")
    close = {}
    for t in tickers:
        price = rng.uniform(50, 300)
        prices = [price]
        for _ in dates[1:]:
            prices.append(prices[-1] * (1 + rng.normal(0.0003, 0.018)))
        close[t] = prices
    df = pd.DataFrame(close, index=dates)

    normalized = (df / df.iloc[0] - 1) * 100
    returns    = df.pct_change().dropna()
    rolling_vol = returns.rolling(21).std() * np.sqrt(252) * 100
    corr        = returns.corr()

    # ── Layout ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 9))
    gs  = gridspec.GridSpec(2, 2, figure=fig,
                            left=0.07, right=0.97, top=0.91, bottom=0.08,
                            hspace=0.38, wspace=0.28)
    ax_ret = fig.add_subplot(gs[0, :])
    ax_vol = fig.add_subplot(gs[1, 0])
    ax_cor = fig.add_subplot(gs[1, 1])

    # Panel 1 — Normalized returns
    for i, t in enumerate(tickers):
        ax_ret.plot(normalized.index, normalized[t],
                    color=CATEGORICAL[i], linewidth=1.6, label=t, alpha=0.9)
    ax_ret.axhline(0, color=PALETTE["muted"], linewidth=0.7, linestyle="--")
    ax_ret.set_title("Cumulative Return vs. Starting Price  (%)", fontweight="bold")
    ax_ret.set_ylabel("Return (%)")
    ax_ret.legend(ncol=5, loc="upper left", fontsize=9)

    # Panel 2 — Rolling 21-day volatility
    for i, t in enumerate(tickers):
        ax_vol.plot(rolling_vol.index, rolling_vol[t],
                    color=CATEGORICAL[i], linewidth=1.4, label=t, alpha=0.85)
    ax_vol.set_title("21-day Rolling Volatility  (annualised %)", fontweight="bold")
    ax_vol.set_ylabel("Volatility (%)")

    # Panel 3 — Correlation heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, ax=ax_cor, annot=True, fmt=".2f", mask=mask,
                cmap=cmap, center=0, linewidths=0.5,
                linecolor=PALETTE["border"],
                annot_kws={"size": 9, "color": PALETTE["text"]},
                cbar_kws={"shrink": 0.75})
    ax_cor.set_title("Return Correlations  (21-day)", fontweight="bold")
    ax_cor.tick_params(axis="both", labelsize=9)
    ax_cor.set_facecolor(PALETTE["surface"])

    fig.suptitle("Tech Stock Performance Dashboard  ·  2023 – 2024",
                 fontsize=15, fontweight="bold", color=PALETTE["text"])
    add_watermark(fig)

    if save:
        fig.savefig(OUTPUT_DIR / "04_stock_dashboard.png", bbox_inches="tight")
        print("  ✓ 04_stock_dashboard.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
