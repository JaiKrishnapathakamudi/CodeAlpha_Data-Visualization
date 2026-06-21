"""
Dataset Generator — creates all sample datasets used in the portfolio.
Run once before generating visualizations.
"""

import numpy as np
import pandas as pd
from pathlib import Path

RNG = np.random.default_rng(42)
DATA_DIR = Path(__file__).parent / "../../assets/data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_global_temperature() -> pd.DataFrame:
    """Simulated global temperature anomaly 1950-2024."""
    years = np.arange(1950, 2025)
    trend = (years - 1950) * 0.018
    noise = RNG.normal(0, 0.12, len(years))
    anomaly = trend + noise
    df = pd.DataFrame({"year": years, "anomaly_c": anomaly.round(3)})
    df.to_csv(DATA_DIR / "global_temperature.csv", index=False)
    return df


def generate_ecommerce_sales() -> pd.DataFrame:
    """Monthly e-commerce sales across product categories."""
    months = pd.date_range("2022-01", "2024-12", freq="MS")
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
    records = []
    for cat in categories:
        base = RNG.uniform(50_000, 200_000)
        seasonal = np.sin(np.linspace(0, 4 * np.pi, len(months))) * base * 0.2
        trend = np.linspace(0, base * 0.3, len(months))
        noise = RNG.normal(0, base * 0.05, len(months))
        sales = (base + seasonal + trend + noise).clip(min=0)
        for m, s in zip(months, sales):
            records.append({"month": m, "category": cat, "sales": round(s, 2)})
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "ecommerce_sales.csv", index=False)
    return df


def generate_customer_segments() -> pd.DataFrame:
    """Customer clustering data: recency, frequency, monetary."""
    n = 800
    segments = {
        "Champions": (0.15, dict(recency=(1, 10), frequency=(20, 50), monetary=(5000, 20000))),
        "Loyal":     (0.20, dict(recency=(10, 30), frequency=(10, 25), monetary=(2000, 8000))),
        "At Risk":   (0.25, dict(recency=(60, 120), frequency=(5, 15), monetary=(500, 3000))),
        "Lost":      (0.25, dict(recency=(150, 365), frequency=(1, 5), monetary=(50, 500))),
        "New":       (0.15, dict(recency=(1, 30), frequency=(1, 3), monetary=(100, 1000))),
    }
    records = []
    for seg, (frac, ranges) in segments.items():
        k = int(n * frac)
        for _ in range(k):
            records.append({
                "segment": seg,
                "recency_days": RNG.integers(*ranges["recency"]),
                "frequency": RNG.integers(*ranges["frequency"]),
                "monetary_usd": round(RNG.uniform(*ranges["monetary"]), 2),
            })
    df = pd.DataFrame(records).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(DATA_DIR / "customer_segments.csv", index=False)
    return df


def generate_stock_prices() -> pd.DataFrame:
    """Simulated OHLCV data for 5 tech stocks."""
    tickers = ["ALFA", "BETA", "GAMA", "DELT", "EPSI"]
    dates = pd.bdate_range("2023-01-01", "2024-12-31")
    records = []
    for ticker in tickers:
        price = RNG.uniform(50, 300)
        for date in dates:
            change = RNG.normal(0.0003, 0.018)
            price *= (1 + change)
            high = price * RNG.uniform(1.001, 1.03)
            low = price * RNG.uniform(0.97, 0.999)
            records.append({
                "date": date, "ticker": ticker,
                "open": round(price, 2), "high": round(high, 2),
                "low": round(low, 2), "close": round(price * RNG.uniform(0.995, 1.005), 2),
                "volume": int(RNG.integers(500_000, 5_000_000)),
            })
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "stock_prices.csv", index=False)
    return df


def generate_survey_results() -> pd.DataFrame:
    """Employee satisfaction survey (Likert 1-5 across 8 dimensions)."""
    n = 500
    dims = ["Work-Life Balance", "Management", "Compensation", "Growth",
            "Culture", "Tools & Tech", "Recognition", "Team Dynamics"]
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"]
    records = []
    for _ in range(n):
        dept = RNG.choice(departments)
        row = {"department": dept, "tenure_years": round(RNG.exponential(3.5), 1)}
        for dim in dims:
            row[dim.replace(" ", "_").replace("&", "and")] = int(RNG.integers(1, 6))
        records.append(row)
    df = pd.DataFrame(records)
    df.to_csv(DATA_DIR / "survey_results.csv", index=False)
    return df


if __name__ == "__main__":
    print("Generating datasets...")
    generate_global_temperature();   print("  ✓ global_temperature.csv")
    generate_ecommerce_sales();      print("  ✓ ecommerce_sales.csv")
    generate_customer_segments();    print("  ✓ customer_segments.csv")
    generate_stock_prices();         print("  ✓ stock_prices.csv")
    generate_survey_results();       print("  ✓ survey_results.csv")
    print("Done — all datasets saved to assets/data/")
