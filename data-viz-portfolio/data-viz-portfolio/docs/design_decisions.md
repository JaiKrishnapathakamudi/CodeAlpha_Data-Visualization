# Design Decisions

This document explains the key choices made in building this visualization portfolio — from colour theory to code architecture.

---

## 1. Dark Theme

**Why dark?**

Most dashboards and data products ship with light backgrounds. A dark theme was chosen deliberately because:

- Charts will be viewed primarily on screens, where dark backgrounds reduce eye strain during extended sessions.
- Accent colours (electric blue, mint, coral) have significantly higher contrast ratios on dark surfaces than on white, making data points more readable at small sizes.
- The aesthetic aligns with modern developer tooling (GitHub, VS Code), making the portfolio feel contemporary.

**Implementation:** All colour constants live in `src/utils/style.py` and are applied globally via `matplotlib.rcParams`. No chart sets any colour inline — everything references the palette tokens. This guarantees a single source of truth.

---

## 2. Colour Palette

The palette is inspired by GitHub's dark-mode design system:

| Token | Hex | Rationale |
|-------|-----|-----------|
| `bg` | `#0D1117` | GitHub dark canvas; near-black without being pure black |
| `surface` | `#161B22` | Slightly lighter — axes sit above the canvas |
| `border` | `#21262D` | Subtle grid lines that don't compete with data |
| `accent` | `#58A6FF` | GitHub's primary link blue — familiar and trustworthy |
| `accent2` | `#3FB950` | Green — positive values, growth, "champions" |
| `accent3` | `#F78166` | Coral — negative values, risk, alerts |
| `accent4` | `#D2A8FF` | Lavender — 4th categorical slot, distinct from blue |
| `accent5` | `#FFA657` | Amber — 5th slot; also used for trend lines / means |

**Contrast compliance:** All accent colours clear WCAG AA (4.5:1) against both `bg` and `surface`.

---

## 3. Chart Type Rationale

| Chart | Type chosen | Why not alternatives |
|-------|-------------|----------------------|
| 01 Climate | Area + scatter + trend | Bar chart loses the temporal continuity; pure line hides the magnitude of individual years |
| 02 E-Commerce | Stacked area | Stacking shows both category and total simultaneously; grouped bars become unreadable at 36 months |
| 03 Customers | Bubble scatter | Three dimensions (R, F, M) need X, Y, and size; colour adds a 4th (segment) — no 2D chart can match this |
| 04 Stocks | Multi-panel | No single chart type shows returns, volatility, AND correlation together; panels keep each story clean |
| 05 Survey | Radar + diverging bar | Radar is the canonical shape-comparison chart for Likert data across many dimensions; the bar provides exact deltas |
| 06 Distributions | Violin + strip | Histograms obscure sample size; box plots hide shape; violin + strip shows both density and individual points |

---

## 4. Annotation Strategy

Every chart has at least one programmatic annotation pointing to the most important finding:

- Annotations are placed with `ax.annotate()` using `arrowprops` for directional emphasis.
- Text boxes use `boxstyle="round,pad=0.3"` with the `surface` fill colour to float above the chart cleanly.
- Font size is kept at 8–9 pt to avoid competing with axis labels.

---

## 5. Grid Philosophy

Grids follow Edward Tufte's data-ink ratio principle:

- **Enabled** horizontally only where the eye needs a ruler (bar/line charts).
- **Colour:** `#21262D` at 60% alpha — visible but not dominant.
- **Spines:** Top and right spines are removed everywhere (`axes.spines.top: False`, `axes.spines.right: False`). Left and bottom spines remain to anchor the axes.

---

## 6. Code Architecture

```
src/
├── utils/style.py          ← palette, rcParams, helpers  (imported by all)
├── data/generate_datasets.py ← reproducible synthetic data
├── visualizations/         ← one file per chart, each exports render(save)
└── build_all.py            ← orchestrator
```

**Each chart module:**
1. Calls `apply_theme()` as its first action.
2. Generates or loads its data.
3. Builds the figure.
4. Calls `add_watermark(fig)`.
5. Saves to `assets/images/` if `save=True` (default).
6. Returns the `Figure` — making it testable without disk I/O.

This architecture means charts can be `import`-ed and called from notebooks, the CLI, or the test suite with no changes.

---

## 7. Reproducibility

All random data uses `numpy.random.default_rng(42)` — the modern NumPy Generator API. The seed is fixed so:

- `python src/build_all.py` produces byte-identical PNGs on every run.
- CI can verify outputs against expected files.
- Colleagues can reproduce results on any machine.

---

## 8. DPI & Export Settings

- **Screen preview:** `figure.dpi = 150` (set in rcParams)
- **Saved files:** `savefig.dpi = 180` — balances file size (~200–400 KB per chart) with sharpness on retina displays.
- **Format:** PNG with `bbox_inches="tight"` to eliminate whitespace padding.
- **Background:** `savefig.facecolor` matches `bg` so the dark background is preserved in the exported file.
