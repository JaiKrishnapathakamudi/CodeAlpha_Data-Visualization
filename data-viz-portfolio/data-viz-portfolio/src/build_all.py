"""
Master build script — generates all portfolio visualizations in one pass.
Usage:  python src/build_all.py
"""

import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

CHARTS = [
    ("01 — Climate Anomaly",       "visualizations.chart_01_climate",      "render"),
    ("02 — E-Commerce Sales",      "visualizations.chart_02_ecommerce",    "render"),
    ("03 — Customer Segments",     "visualizations.chart_03_segments",     "render"),
    ("04 — Stock Dashboard",       "visualizations.chart_04_stocks",       "render"),
    ("05 — Survey Radar",          "visualizations.chart_05_survey",       "render"),
    ("06 — Revenue Distributions", "visualizations.chart_06_distributions","render"),
]


def main():
    print("\n" + "=" * 60)
    print("  Data Visualization Portfolio — Build Script")
    print("=" * 60)

    t0 = time.time()
    success, failed = 0, []

    for label, module, fn in CHARTS:
        print(f"\n▸ {label}")
        try:
            import importlib
            mod = importlib.import_module(module)
            getattr(mod, fn)(save=True)
            success += 1
        except Exception as exc:
            print(f"  ✗ FAILED — {exc}")
            failed.append(label)

    elapsed = time.time() - t0
    print("\n" + "=" * 60)
    print(f"  Done in {elapsed:.1f}s  |  {success}/{len(CHARTS)} charts generated")
    if failed:
        print("  Failed:", ", ".join(failed))
    print(f"  Output → assets/images/")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
