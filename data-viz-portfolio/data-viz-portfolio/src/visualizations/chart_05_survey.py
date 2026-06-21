"""
Chart 05 — Employee Satisfaction Survey
Type: Radar (spider) chart per department + diverging bar
Story: Surface where each department excels or needs attention.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, CATEGORICAL, OUTPUT_DIR


DIMS = ["Work-Life\nBalance", "Management", "Compensation", "Growth",
        "Culture", "Tools &\nTech", "Recognition", "Team\nDynamics"]
DIM_KEYS = ["Work-Life_Balance", "Management", "Compensation", "Growth",
            "Culture", "Tools_and_Tech", "Recognition", "Team_Dynamics"]
DEPARTMENTS = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]


def radar_patch(ax, values, color, label, alpha=0.25):
    N = len(values)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    vals   = values.tolist() + values[:1].tolist()
    ang    = angles + angles[:1]
    ax.plot(ang, vals, color=color, linewidth=2, label=label)
    ax.fill(ang, vals, color=color, alpha=alpha)


def render(save: bool = True) -> plt.Figure:
    apply_theme()

    rng = np.random.default_rng(42)
    records = []
    for dept in DEPARTMENTS:
        for _ in range(80):
            row = {"department": dept}
            for k in DIM_KEYS:
                row[k] = int(rng.integers(1, 6))
            records.append(row)
    df = pd.DataFrame(records)
    dept_means = df.groupby("department")[DIM_KEYS].mean()

    fig = plt.figure(figsize=(15, 7))
    gs  = gridspec.GridSpec(1, 2, figure=fig,
                            left=0.04, right=0.97, top=0.88, bottom=0.08,
                            wspace=0.1)

    # ── Radar ─────────────────────────────────────────────────────────────────
    N = len(DIM_KEYS)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    ax_radar = fig.add_subplot(gs[0], polar=True)
    ax_radar.set_theta_offset(np.pi / 2)
    ax_radar.set_theta_direction(-1)
    ax_radar.set_thetagrids(np.degrees(angles), DIMS, fontsize=8.5,
                             color=PALETTE["muted"])
    ax_radar.set_ylim(0, 5)
    ax_radar.set_yticks([1, 2, 3, 4, 5])
    ax_radar.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=7,
                              color=PALETTE["muted"])
    ax_radar.set_facecolor(PALETTE["surface"])
    ax_radar.spines["polar"].set_color(PALETTE["border"])
    ax_radar.grid(color=PALETTE["border"], linewidth=0.5, alpha=0.7)

    for i, dept in enumerate(DEPARTMENTS):
        radar_patch(ax_radar, dept_means.loc[dept].values, CATEGORICAL[i], dept)

    ax_radar.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1),
                    fontsize=9, framealpha=0.9)
    ax_radar.set_title("Satisfaction by Department\n(Likert 1–5)",
                        fontsize=12, fontweight="bold", color=PALETTE["text"], pad=18)

    # ── Diverging bar (gap vs average) ────────────────────────────────────────
    ax_bar = fig.add_subplot(gs[1])
    overall_mean = dept_means.mean()
    gaps = dept_means - overall_mean

    y_pos = np.arange(len(DIM_KEYS))
    bar_width = 0.12
    for i, dept in enumerate(DEPARTMENTS):
        vals = gaps.loc[dept].values
        ax_bar.barh(y_pos - i * bar_width,
                    vals, height=bar_width,
                    color=CATEGORICAL[i], alpha=0.8, label=dept)

    ax_bar.axvline(0, color=PALETTE["muted"], linewidth=1)
    ax_bar.set_yticks(y_pos - (len(DEPARTMENTS) - 1) * bar_width / 2)
    ax_bar.set_yticklabels([d.replace("\n", " ") for d in DIMS], fontsize=9)
    ax_bar.set_xlabel("Gap vs. Company Average (Likert points)", labelpad=8)
    ax_bar.set_title("Dimension Gaps vs. Overall Mean",
                     fontsize=12, fontweight="bold", color=PALETTE["text"])

    fig.suptitle("Employee Satisfaction Survey Analysis  ·  N = 480",
                 fontsize=15, fontweight="bold", color=PALETTE["text"])
    add_watermark(fig)

    if save:
        fig.savefig(OUTPUT_DIR / "05_survey_radar.png", bbox_inches="tight")
        print("  ✓ 05_survey_radar.png")
    return fig


if __name__ == "__main__":
    render()
    plt.show()
