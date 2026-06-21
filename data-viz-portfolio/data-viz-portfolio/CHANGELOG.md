# Changelog

All notable changes are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) · Versioning: [SemVer](https://semver.org/).

---

## [Unreleased]

### Planned
- Interactive Plotly HTML exports for each chart
- Choropleth world-map (geospatial module)
- Sankey diagram for user funnel analysis
- Animated time-series (matplotlib.animation)
- Dark/light theme toggle in portfolio web app
- Docker containerisation

---

## [1.0.0] — 2025-06-20

### Added
- **Chart 01** — Global Temperature Anomaly: area chart with Savitzky-Golay trend, peak annotation
- **Chart 02** — E-Commerce Sales Dashboard: stacked area + YoY diverging bar inset
- **Chart 03** — Customer RFM Segmentation: bubble scatter with quadrant overlays and 5 segments
- **Chart 04** — Stock Performance Dashboard: 3-panel (cumulative returns, volatility, correlation heatmap)
- **Chart 05** — Employee Satisfaction Survey: polar radar + diverging bar gap analysis
- **Chart 06** — Revenue Distribution Analysis: violin + strip + custom IQR summary panel
- **Flask backend** (`app.py`) with REST API: `/api/charts`, `/api/image/<id>`, `/api/stats`, `/api/build`
- **Portfolio web app** (`portfolio_app.html`): self-contained dark-theme gallery with filter, search, modal, download
- **Shared theme** (`src/utils/style.py`): GitHub-inspired dark palette, rcParams, watermark helper
- **Reproducible synthetic datasets** (`src/data/generate_datasets.py`) with `numpy.random.default_rng(42)`
- **One-command build** (`src/build_all.py`) — 6/6 charts in ~8 seconds
- **Pytest suite** (`tests/test_charts.py`) — 8/8 tests passing across Python 3.10–3.12
- **GitHub Actions CI** — matrix build on Python 3.10, 3.11, 3.12
- **GitHub Actions Release** — auto-packages and publishes on version tags
- **Jupyter notebook** walkthrough (`notebooks/portfolio_walkthrough.ipynb`)
- **Design decisions doc** (`docs/design_decisions.md`) — rationale for every key choice
- All standard GitHub community files: README, LICENSE (MIT), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CODEOWNERS, PR template, issue templates
