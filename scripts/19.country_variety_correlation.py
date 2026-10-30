
# Step 19: Analyse price-rating correlations by country and variety

import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"

OUTPUT_FILE = (
    PROJECT_DIR
    / "reports"
    / "country_variety_correlation.csv"
)

# --------------------------------------------------
# 2. Load the deduplicated analytical dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 65)
print("COUNTRY–VARIETY PRICE-RATING CORRELATION ANALYSIS")
print("=" * 65)

print(f"\nDataset rows loaded: {len(df):,}")

# --------------------------------------------------
# 3. Prepare the data
# --------------------------------------------------

# Convert price and rating columns to numeric values.
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["points"] = pd.to_numeric(df["points"], errors="coerce")

# Keep only rows with usable prices, ratings, countries and varieties.
df = df.dropna(
    subset=["price", "points", "country", "variety"]
).copy()

# Exclude zero or negative prices because this analysis concerns
# meaningful positive listed prices.
df = df[df["price"] > 0].copy()

print(f"Valid records for analysis: {len(df):,}")

# --------------------------------------------------
# 4. Analyse each country–variety combination
# --------------------------------------------------

# Require at least 50 records per combination.
# Small groups can produce unstable correlation estimates.
MIN_RECORDS = 50

results = []

grouped = df.groupby(["country", "variety"], observed=True)

for (country, variety), group in grouped:

    # Ignore combinations with too few observations.
    if len(group) < MIN_RECORDS:
        continue

    # Correlations are undefined when either variable is constant.
    if group["price"].nunique() < 2 or group["points"].nunique() < 2:
        continue

    pearson_corr = group["price"].corr(
        group["points"],
        method="pearson"
    )

    spearman_corr = group["price"].corr(
        group["points"],
        method="spearman"
    )

    results.append({
        "country": country,
        "variety": variety,
        "record_count": len(group),
        "mean_price": round(group["price"].mean(), 2),
        "median_price": round(group["price"].median(), 2),
        "mean_rating": round(group["points"].mean(), 2),
        "pearson_correlation": round(pearson_corr, 4),
        "spearman_correlation": round(spearman_corr, 4),
        "rated_90_plus_count": int((group["points"] >= 90).sum()),
        "rated_90_plus_pct": round(
            (group["points"] >= 90).mean() * 100, 2
        )
    })

# --------------------------------------------------
# 5. Create and save the results
# --------------------------------------------------

results_df = pd.DataFrame(results)

if results_df.empty:
    raise ValueError(
        "No country-variety groups met the minimum record requirement."
    )

# Sort by Spearman correlation, from highest to lowest.
results_df = results_df.sort_values(
    by="spearman_correlation",
    ascending=False
)

results_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nMinimum records per combination: {MIN_RECORDS}")
print(f"Country-variety combinations analysed: {len(results_df):,}")
print(f"Report saved to: {OUTPUT_FILE}")

# --------------------------------------------------
# 6. Display key findings
# --------------------------------------------------

columns_to_display = [
    "country",
    "variety",
    "record_count",
    "mean_price",
    "mean_rating",
    "pearson_correlation",
    "spearman_correlation",
    "rated_90_plus_pct"
]

print("\nTOP 10 COMBINATIONS BY SPEARMAN CORRELATION")
print(
    results_df[columns_to_display]
    .head(10)
    .to_string(index=False)
)

print("\nBOTTOM 10 COMBINATIONS BY SPEARMAN CORRELATION")
print(
    results_df[columns_to_display]
    .tail(10)
    .sort_values("spearman_correlation")
    .to_string(index=False)
)

print("\nSTRONGEST NEGATIVE PEARSON CORRELATIONS")
print(
    results_df.nsmallest(10, "pearson_correlation")[
        columns_to_display
    ].to_string(index=False)
)

print("\n" + "=" * 65)
print("COUNTRY–VARIETY CORRELATION ANALYSIS COMPLETED")
print("=" * 65)
