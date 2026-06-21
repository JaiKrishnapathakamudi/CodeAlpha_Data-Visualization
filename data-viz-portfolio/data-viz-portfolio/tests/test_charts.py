"""
Test suite — verifies each chart module renders without error
and writes the expected PNG file to assets/images/.
"""

import pytest
import importlib
import matplotlib
matplotlib.use("Agg")   # headless backend for CI
from pathlib import Path

SRC = Path(__file__).parent.parent / "src"
IMAGES = SRC.parent / "assets" / "images"

MODULES = [
    ("visualizations.chart_01_climate",       "01_climate_anomaly.png"),
    ("visualizations.chart_02_ecommerce",     "02_ecommerce_sales.png"),
    ("visualizations.chart_03_segments",      "03_customer_segments.png"),
    ("visualizations.chart_04_stocks",        "04_stock_dashboard.png"),
    ("visualizations.chart_05_survey",        "05_survey_radar.png"),
    ("visualizations.chart_06_distributions", "06_distributions.png"),
]


@pytest.fixture(scope="session", autouse=True)
def add_src_to_path():
    import sys
    sys.path.insert(0, str(SRC))


@pytest.mark.parametrize("module,expected_file", MODULES)
def test_chart_renders(module, expected_file):
    """Each chart module must import, call render(), and produce a PNG."""
    mod = importlib.import_module(module)
    fig = mod.render(save=True)

    # Figure object must be returned
    import matplotlib.pyplot as plt
    assert isinstance(fig, plt.Figure), f"{module}.render() must return a Figure"

    # Output file must exist
    output_path = IMAGES / expected_file
    assert output_path.exists(), f"Expected output not found: {output_path}"
    assert output_path.stat().st_size > 5_000, f"PNG suspiciously small: {output_path}"

    plt.close("all")


def test_images_directory_exists():
    assert IMAGES.is_dir(), "assets/images/ directory not found"


def test_all_outputs_present():
    expected = {f for _, f in MODULES}
    found = {p.name for p in IMAGES.glob("*.png")}
    missing = expected - found
    assert not missing, f"Missing chart outputs: {missing}"
