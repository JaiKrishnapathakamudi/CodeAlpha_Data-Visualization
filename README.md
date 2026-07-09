<div align="center">

# 📊 Data Visualization Portfolio

**Transforming raw data into compelling visual stories**

[![CI](https://img.shields.io/github/actions/workflow/status/<your-username>/data-viz-portfolio/ci.yml?branch=main&label=CI&logo=github)](https://github.com/<your-username>/data-viz-portfolio/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?logo=python&logoColor=white)](https://python.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10-orange?logo=python)](https://matplotlib.org)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13-teal)](https://seaborn.pydata.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Charts](https://img.shields.io/badge/Charts-6%2F6-purple)]()
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20passing-brightgreen)]()

</div>

---

## 📖 Overview

Six production-quality data visualizations covering real-world analytical scenarios.
Every chart shares a unified dark theme, tells a clear data story, and is backed by
a reproducible Python pipeline and a Flask REST API.

| # | Chart | Type | Domain |
|---|-------|------|--------|
| 01 | [Global Temperature Anomaly](#-01--global-temperature-anomaly) | Area + trend line | Climate Science |
| 02 | [E-Commerce Dashboard](#-02--e-commerce-revenue-dashboard) | Stacked area + YoY bar | Business Analytics |
| 03 | [Customer Segmentation](#-03--customer-rfm-segmentation) | Bubble scatter (RFM) | Marketing |
| 04 | [Stock Dashboard](#-04--stock-performance-dashboard) | 3-panel multi-chart | Finance |
| 05 | [Survey Radar](#-05--employee-satisfaction-survey) | Radar + diverging bar | HR Analytics |
| 06 | [Revenue Distributions](#-06--revenue-distribution-analysis) | Violin + strip + box | Statistics |

---

## 🚀 Quickstart

### Option A — Run everything in 3 commands

```bash
git clone https://github.com/<your-username>/data-viz-portfolio.git
cd data-viz-portfolio
pip install -r requirements.txt && python src/build_all.py
```

### Option B — Make targets

```bash
make install    # install dependencies
make build      # generate all 6 charts → assets/images/
make test       # run 8 tests
make run-api    # start Flask API on http://localhost:5000
```

### Option C — Single chart

```bash
python src/visualizations/chart_01_climate.py
# saves PNG + opens interactive window
```

---

## 📁 Repository Structure

```
data-viz-portfolio/
│
├── 📂 src/
│   ├── visualizations/
│   │   ├── chart_01_climate.py          # Area chart — temperature anomaly
│   │   ├── chart_02_ecommerce.py        # Stacked area — e-commerce revenue
│   │   ├── chart_03_segments.py         # Bubble scatter — RFM segmentation
│   │   ├── chart_04_stocks.py           # 3-panel — stock dashboard
│   │   ├── chart_05_survey.py           # Radar — employee survey
│   │   └── chart_06_distributions.py   # Violin — revenue distributions
│   ├── data/
│   │   └── generate_datasets.py         # Reproducible synthetic data
│   ├── utils/
│   │   └── style.py                     # Shared palette, rcParams, watermark
│   └── build_all.py                     # One-command orchestrator
│
├── 📂 assets/images/                    # Generated PNG outputs (180 DPI)
├── 📂 notebooks/                        # Jupyter EDA walkthrough
├── 📂 tests/                            # Pytest suite (8 tests)
├── 📂 docs/                             # Design decisions
├── 📂 .github/                          # CI, release, issue templates, PR template
│
├── app.py                               # Flask REST API backend
├── portfolio_app.html                   # Self-contained frontend gallery
├── requirements.txt                     # Pinned runtime deps
├── requirements-dev.txt                 # Dev tools (black, flake8, etc.)
├── pyproject.toml                       # Modern Python packaging
├── setup.py / setup.cfg                 # Legacy packaging support
├── Makefile                             # Convenience targets
├── pytest.ini                           # Test configuration
├── .env.example                         # Environment variable template
└── .gitignore                           # Comprehensive ignore rules
```

---

## 🖼️ Chart Gallery

### 🌡️ 01 · Global Temperature Anomaly

> **Story:** 75 years of climate data visualized as a dual-fill area chart. Red fills mark warmer-than-baseline years; blue marks cooler. A Savitzky-Golay smoothed curve exposes the underlying trend.

![Climate](assets/images/01_climate_anomaly.png)

**Key insight:** +1.3 °C average warming over 75 years · **Tools:** Matplotlib, SciPy

---

### 🛒 02 · E-Commerce Revenue Dashboard

> **Story:** Monthly revenue across five product categories stacked to show both individual performance and total. The side panel turns 36 months of numbers into a YoY growth at-a-glance.

![E-Commerce](assets/images/02_ecommerce_sales.png)

**Key insight:** Electronics drives 38% of total revenue · **Tools:** Matplotlib GridSpec

---

### 🎯 03 · Customer RFM Segmentation

> **Story:** Three dimensions in one view — Recency (X), Frequency (Y), Lifetime Value (bubble size) — let marketers instantly see Champions vs Lost customers and where to focus retention.

![Segments](assets/images/03_customer_segments.png)

**Key insight:** Champions (15% of customers) generate 62% of LTV · **Tools:** Matplotlib

---

### 📈 04 · Stock Performance Dashboard

> **Story:** Three coordinated panels — cumulative returns, 21-day rolling volatility, and a correlation heatmap — tell the full story of a 5-stock portfolio.

![Stocks](assets/images/04_stock_dashboard.png)

**Key insight:** ALFA & BETA show 0.82 correlation in downturns · **Tools:** Matplotlib, Seaborn

---

### 📋 05 · Employee Satisfaction Survey

> **Story:** A polar radar chart overlays six departments across eight dimensions simultaneously. The diverging bar companion quantifies each department's gap vs. the company mean.

![Survey](assets/images/05_survey_radar.png)

**Key insight:** Engineering leads on Tools; HR trails on Compensation · **Tools:** Matplotlib Polar

---

### 📦 06 · Revenue Distribution Analysis

> **Story:** Violin + strip plots expose both shape and individual transactions that box plots hide. A custom IQR summary with mean diamonds gives precise statistical context.

![Distributions](assets/images/06_distributions.png)

**Key insight:** Electronics has 3× more high-value outliers than Books · **Tools:** Seaborn, Matplotlib

---

## ⚙️ Backend API

Start the Flask server:

```bash
python app.py
# → http://localhost:5000
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check + endpoint list |
| `GET` | `/api/charts` | All charts (supports `?tag=` `?tool=` `?q=`) |
| `GET` | `/api/charts/<id>` | Single chart metadata |
| `GET` | `/api/image/<id>` | Chart PNG binary |
| `GET` | `/api/stats` | Portfolio statistics |
| `POST` | `/api/build` | Trigger full chart rebuild |

---

## 🎨 Visual Identity

All charts share a GitHub-inspired dark palette defined in `src/utils/style.py`:

| Token | Hex | Role |
|-------|-----|------|
| `bg` | `#0D1117` | Canvas background |
| `surface` | `#161B22` | Axes surface |
| `accent` | `#58A6FF` | Primary highlight (blue) |
| `accent2` | `#3FB950` | Positive / growth (green) |
| `accent3` | `#F78166` | Negative / risk (coral) |
| `accent4` | `#D2A8FF` | 4th series (lavender) |
| `accent5` | `#FFA657` | 5th series / trend (amber) |
| `text` | `#E6EDF3` | Primary labels |
| `muted` | `#8B949E` | Secondary labels |

---

## 🛠️ Tech Stack

| Library | Version | Role |
|---------|---------|------|
| Matplotlib | 3.10.8 | Core rendering engine |
| Seaborn | 0.13.2 | Statistical plot helpers |
| Pandas | 3.0.2 | Data wrangling |
| NumPy | 2.4.4 | Numerical computing |
| SciPy | 1.17.1 | Savitzky-Golay smoothing |
| Plotly | 6.8.0 | Interactive HTML exports |
| scikit-learn | 1.8.0 | Clustering utilities |
| Flask | 3.x | REST API backend |
| Pytest | 9.1.1 | Test suite (8/8 passing) |

---

## 🧪 Testing

```bash
pytest tests/ -v                          # run all 8 tests
pytest tests/ -v --cov=src               # with coverage
```

Tests verify that every chart module:
1. Imports without errors
2. `render(save=True)` returns a `plt.Figure`
3. Writes a PNG to `assets/images/` (> 5 KB)

---

## 📐 Design Principles

1. **Story-first** — every chart has one headline insight; annotations point directly to it
2. **Dark canvas** — reduces eye strain; accent colours have higher contrast on dark backgrounds
3. **Single palette source** — all colours reference tokens in `style.py` — zero hard-coded hex
4. **Data-ink ratio** — top/right spines removed; grid is subtle; no chart junk
5. **Reproducibility** — fixed `numpy.random.default_rng(42)` seeds; identical output every run
6. **Testable by design** — `render(save=False)` returns the Figure for headless CI testing

---

## 📄 License

[MIT](LICENSE) — free to use, adapt, and build on. Attribution appreciated.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide on adding charts, running tests, and submitting PRs.

---

<div align="center">
Built with Python · Matplotlib · Seaborn · Flask
</div>
