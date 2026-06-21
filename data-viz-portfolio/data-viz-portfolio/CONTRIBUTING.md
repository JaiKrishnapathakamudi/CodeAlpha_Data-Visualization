# Contributing to Data Visualization Portfolio

Thank you for your interest! Contributions of all kinds are welcome — new charts,
bug fixes, documentation improvements, or design enhancements.

---

## 🚀 Getting Started

### 1. Fork & clone

```bash
git clone https://github.com/<your-username>/data-viz-portfolio.git
cd data-viz-portfolio
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 3. Verify the setup works

```bash
python src/build_all.py         # should print 6/6 charts generated
pytest tests/ -v                # should print 8/8 passed
```

---

## 🗂️ Project Structure

```
src/
├── utils/style.py          ← shared palette & rcParams  (always import this first)
├── data/generate_datasets.py
├── visualizations/         ← one module per chart
└── build_all.py            ← orchestrator
tests/
assets/images/              ← generated PNG outputs
```

---

## ✨ Adding a New Chart

### Step 1 — Create the module

```
src/visualizations/chart_07_yourname.py
```

Every chart module **must**:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.style import apply_theme, add_watermark, PALETTE, OUTPUT_DIR

def render(save: bool = True) -> plt.Figure:
    apply_theme()          # ← always first
    # ... your chart code ...
    add_watermark(fig)     # ← always before save
    if save:
        fig.savefig(OUTPUT_DIR / "07_yourname.png", bbox_inches="tight")
    return fig             # ← always return the Figure
```

### Step 2 — Register in build_all.py

```python
("07 — Your Chart Title", "visualizations.chart_07_yourname", "render"),
```

### Step 3 — Add a test

```python
# tests/test_charts.py — add to MODULES list:
("visualizations.chart_07_yourname", "07_yourname.png"),
```

### Step 4 — Document it

Add an entry to the **Chart Gallery** section in `README.md`.

---

## 🎨 Style Rules

- **Always** use palette tokens from `style.py` — never hard-code hex colours
- **Always** call `apply_theme()` as the first line of `render()`
- Use `CATEGORICAL[0..6]` for sequential series colours
- Remove top and right spines — this is set globally but don't re-enable them
- Titles: `fontsize=13-15`, `fontweight="bold"`, `color=PALETTE["text"]`
- All output PNGs: `dpi=180`, `bbox_inches="tight"`

---

## 🧪 Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Single chart
pytest tests/test_charts.py::test_chart_renders[visualizations.chart_01_climate-01_climate_anomaly.png] -v
```

---

## 📋 Commit Convention

```
feat: add candlestick OHLC chart (#8)
fix: resolve seaborn deprecation warning in chart_06 (#7)
style: improve radar chart label spacing (#6)
docs: update README with chart 07 gallery entry (#5)
test: add parametrised test for chart_07 (#4)
chore: pin numpy to 2.4.4 in requirements (#3)
```

---

## 📤 Submitting a Pull Request

1. Create a feature branch: `git checkout -b feat/chart-07-candlestick`
2. Make your changes following the rules above
3. Run `python src/build_all.py` and `pytest tests/ -v` — both must pass
4. Commit and push your branch
5. Open a PR against `main` and fill in the PR template
6. CI must be green before merge

---

## 💬 Questions?

Open a [GitHub Discussion](https://github.com/<your-username>/data-viz-portfolio/discussions)
or file an [Issue](https://github.com/<your-username>/data-viz-portfolio/issues).
