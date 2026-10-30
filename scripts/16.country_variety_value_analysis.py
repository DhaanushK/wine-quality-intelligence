
from pathlib import Path
import pandas as pd

# Define the project and dataset paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)
OUTPUT_PATH = (
    PROJECT_DIR / "reports" / "country_variety_value_analysis.csv"
)

df = pd.read_csv(DATA_PATH)

# Keep records that can be used in this comparison
df = df.loc[
    df["price"].notna()
    & (df["price"] > 0)
    & df["points"].notna()
    & df["country"].notna()
    & df["variety"].notna()
].copy()

# Apply the exploratory thresholds
candidates = df.loc[
    (df["price"] <= 30)
    & (df["points"] >= 90)
].copy()

# Summarize each country-variety combination
summary = (
    candidates.groupby(["country", "variety"])
    .agg(
        record_count=("points", "size"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("points", "mean"),
        median_rating=("points", "median"),
        highest_rating=("points", "max"),
    )
    .reset_index()
)

# Keep groups with at least 20 matching records.
# This reduces attention on combinations represented by very few records.
reliable_size_groups = summary.loc[
    summary["record_count"] >= 20
].copy()

# Sort by mean rating, then mean price
ranked = reliable_size_groups.sort_values(
    ["mean_rating", "mean_price", "record_count"],
    ascending=[False, True, False]
)

print("\n===== TOP COUNTRY-VARIETY COMBINATIONS =====")
print(
    ranked.head(20).round(2).to_string(index=False)
)

print("\n===== LOWER-MEAN-PRICE COMBINATIONS =====")
lower_price_groups = reliable_size_groups.sort_values(
    ["mean_price", "mean_rating"],
    ascending=[True, False]
)

print(
    lower_price_groups.head(20).round(2).to_string(index=False)
)

# Save the full grouped results for later reporting and dashboard use
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
ranked.to_csv(OUTPUT_PATH, index=False)

print(f"\nCountry-variety results saved to: {OUTPUT_PATH}")
print(f"Groups with at least 20 matching records: {len(ranked):,}")
print("\nAnalysis completed. Source datasets were not modified.")
