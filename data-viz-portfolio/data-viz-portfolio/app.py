"""
Backend API Server — Flask
Serves chart metadata and PNG images as a REST API.

Endpoints:
  GET /              → health check
  GET /api/charts    → list all charts with metadata
  GET /api/charts/<id> → single chart metadata
  GET /api/image/<id>  → chart PNG (binary)
  GET /api/stats     → portfolio stats
  POST /api/build    → trigger rebuild of all charts

Run:
  python app.py
  → http://localhost:5000
"""

import os
import json
import subprocess
from pathlib import Path
from flask import Flask, jsonify, send_file, abort, request
from flask import make_response

BASE_DIR   = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "assets" / "images"
SRC_DIR    = BASE_DIR / "src"

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# ── Chart metadata ─────────────────────────────────────────────────────────────
CHARTS = [
    {
        "id": "01_climate_anomaly",
        "num": "01",
        "title": "Global Temperature Anomaly",
        "subtitle": "1950 – 2024",
        "type": "Area Chart + Trend Line",
        "tools": ["Matplotlib", "SciPy"],
        "tags": ["Climate", "Time Series", "Annotation"],
        "story": (
            "75 years of rising global temperatures as a dual-fill area chart. "
            "Red fills mark years warmer than the pre-industrial baseline; blue marks cooler years. "
            "A Savitzky-Golay smoothed curve exposes the underlying trend."
        ),
        "key_insight": "+1.3°C average warming over 75 years",
        "filename": "01_climate_anomaly.png",
    },
    {
        "id": "02_ecommerce_sales",
        "num": "02",
        "title": "E-Commerce Revenue Dashboard",
        "subtitle": "2022 – 2024",
        "type": "Stacked Area + YoY Bar",
        "tools": ["Matplotlib", "GridSpec"],
        "tags": ["Business", "Comparison", "Multi-panel"],
        "story": (
            "Monthly revenue across five product categories stacked to reveal both "
            "individual performance and the aggregate trend. The side panel computes "
            "year-over-year growth rates — green bars signal growth, red bars flag decline."
        ),
        "key_insight": "Electronics drives 38% of total revenue",
        "filename": "02_ecommerce_sales.png",
    },
    {
        "id": "03_customer_segments",
        "num": "03",
        "title": "Customer RFM Segmentation",
        "subtitle": "800 Customers · 5 Segments",
        "type": "Bubble Scatter Plot",
        "tools": ["Matplotlib"],
        "tags": ["Marketing", "Clustering", "Bubble Chart"],
        "story": (
            "Three dimensions encoded in a single view: Recency (X, inverted), "
            "Purchase Frequency (Y), and Lifetime Value (bubble size). Colour encodes "
            "segment — Champions, Loyal, At Risk, Lost, New."
        ),
        "key_insight": "Champions (15%) generate 62% of LTV",
        "filename": "03_customer_segments.png",
    },
    {
        "id": "04_stock_dashboard",
        "num": "04",
        "title": "Stock Performance Dashboard",
        "subtitle": "5 Tickers · 2 Years",
        "type": "3-Panel Multi-Chart",
        "tools": ["Matplotlib", "Seaborn"],
        "tags": ["Finance", "Multi-panel", "Heatmap"],
        "story": (
            "Three coordinated panels: cumulative returns since inception, "
            "21-day rolling annualised volatility, and a lower-triangle correlation heatmap. "
            "Demonstrates GridSpec composition of multiple chart types."
        ),
        "key_insight": "ALFA & BETA show 0.82 correlation in downturns",
        "filename": "04_stock_dashboard.png",
    },
    {
        "id": "05_survey_radar",
        "num": "05",
        "title": "Employee Satisfaction Survey",
        "subtitle": "480 Employees · 6 Departments",
        "type": "Radar + Diverging Bar",
        "tools": ["Matplotlib", "Polar Axes"],
        "tags": ["HR", "Radar Chart", "Survey"],
        "story": (
            "A polar radar chart overlays six departments across eight satisfaction "
            "dimensions simultaneously. The companion diverging bar chart quantifies "
            "each department's gap vs. the company mean."
        ),
        "key_insight": "Engineering leads on Tools; HR trails on Compensation",
        "filename": "05_survey_radar.png",
    },
    {
        "id": "06_distributions",
        "num": "06",
        "title": "Revenue Distribution Analysis",
        "subtitle": "~1,000 Transactions",
        "type": "Violin + Strip + IQR Summary",
        "tools": ["Seaborn", "Matplotlib"],
        "tags": ["Statistics", "Distribution", "Seaborn"],
        "story": (
            "Violin plots expose distribution shape; strip plots reveal individual "
            "transactions. Together they show density and outliers that box plots hide. "
            "Custom IQR summary bars with mean diamonds complete the statistical picture."
        ),
        "key_insight": "Electronics has 3× more high-value outliers than Books",
        "filename": "06_distributions.png",
    },
]

CHARTS_BY_ID = {c["id"]: c for c in CHARTS}


def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def health():
    return jsonify({
        "status": "ok",
        "service": "DataViz Portfolio API",
        "version": "1.0.0",
        "charts_available": len(CHARTS),
        "endpoints": [
            "GET  /api/charts",
            "GET  /api/charts/<id>",
            "GET  /api/image/<id>",
            "GET  /api/stats",
            "POST /api/build",
        ],
    })


@app.route("/api/charts")
def list_charts():
    tag  = request.args.get("tag")
    tool = request.args.get("tool")
    q    = request.args.get("q", "").lower()

    results = CHARTS
    if tag:
        results = [c for c in results if tag in c["tags"]]
    if tool:
        results = [c for c in results if tool in c["tools"]]
    if q:
        results = [c for c in results if q in c["title"].lower() or q in c["story"].lower()]

    resp = make_response(jsonify({"count": len(results), "charts": results}))
    return add_cors(resp)


@app.route("/api/charts/<chart_id>")
def get_chart(chart_id):
    chart = CHARTS_BY_ID.get(chart_id)
    if not chart:
        abort(404, description=f"Chart '{chart_id}' not found")
    resp = make_response(jsonify(chart))
    return add_cors(resp)


@app.route("/api/image/<chart_id>")
def get_image(chart_id):
    chart = CHARTS_BY_ID.get(chart_id)
    if not chart:
        abort(404, description=f"Chart '{chart_id}' not found")
    img_path = IMAGES_DIR / chart["filename"]
    if not img_path.exists():
        abort(404, description="Image file not found — run build first")
    return send_file(img_path, mimetype="image/png",
                     as_attachment=False,
                     download_name=chart["filename"])


@app.route("/api/stats")
def stats():
    images_found = sum(1 for c in CHARTS if (IMAGES_DIR / c["filename"]).exists())
    all_tags  = sorted({t for c in CHARTS for t in c["tags"]})
    all_tools = sorted({t for c in CHARTS for t in c["tools"]})
    resp = make_response(jsonify({
        "total_charts":   len(CHARTS),
        "images_on_disk": images_found,
        "unique_tags":    all_tags,
        "unique_tools":   all_tools,
        "image_dir":      str(IMAGES_DIR),
        "python_version": os.popen("python3 --version").read().strip(),
    }))
    return add_cors(resp)


@app.route("/api/build", methods=["POST"])
def build():
    """Trigger a rebuild of all charts."""
    build_script = SRC_DIR / "build_all.py"
    if not build_script.exists():
        abort(500, description="build_all.py not found")
    try:
        result = subprocess.run(
            ["python3", str(build_script)],
            capture_output=True, text=True, timeout=120
        )
        resp = make_response(jsonify({
            "success": result.returncode == 0,
            "stdout":  result.stdout,
            "stderr":  result.stderr,
        }))
        return add_cors(resp)
    except subprocess.TimeoutExpired:
        abort(504, description="Build timed out after 120 seconds")


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  📊 DataViz Portfolio — Backend API")
    print("=" * 55)
    print(f"  Charts loaded  : {len(CHARTS)}")
    print(f"  Images on disk : {sum(1 for c in CHARTS if (IMAGES_DIR/c['filename']).exists())}")
    print(f"  Listening on   : http://localhost:5000")
    print("=" * 55 + "\n")
    app.run(debug=True, port=5000, host="0.0.0.0")
