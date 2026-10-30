from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)
OUTPUT_PATH = (
    PROJECT_DIR / "reports" / "overall_country_variety_analysis.csv"
)

# Load the deduplicated dataset
df = pd.read_csv(DATA_PATH)

# Keep records with valid prices, ratings, country, and variety
analysis_df = df.loc[
    df["price"].notna()
    & (df["price"] > 0)
    & df["points"].notna()
    & df["country"].notna()
    & df["variety"].notna()
].copy()

# Group all eligible records by country and variety
summary = (
    analysis_df.groupby(["country", "variety"])
    .agg(
        record_count=("points", "size"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("points", "mean"),
        median_rating=("points", "median"),
        wines_rated_90_plus=("points", lambda s: (s >= 90).sum()),
    )
    .reset_index()
)

# Calculate the percentage rated 90 or higher
summary["percent_rated_90_plus"] = (
    summary["wines_rated_90_plus"]
    / summary["record_count"]
    * 100
)

# Restrict comparisons to combinations with at least 30 records
# This is a practical screening rule, not a statistical guarantee.
eligible_groups = summary.loc[
    summary["record_count"] >= 30
].copy()

# Save the full eligible summary for reporting and dashboard work
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
eligible_groups.to_csv(OUTPUT_PATH, index=False)

print("\n===== OVERALL COUNTRY-VARIETY ANALYSIS =====")
print(f"Priced records analyzed: {len(analysis_df):,}")
print(f"Country-variety groups before size filter: {len(summary):,}")
print(f"Groups with at least 30 records: {len(eligible_groups):,}")

print("\n===== HIGHEST MEAN RATINGS =====")
print(
    eligible_groups.sort_values(
        ["mean_rating", "record_count"],
        ascending=[False, False]
    )
    .head(15)
    .round(2)
    .to_string(index=False)
)

print("\n===== LOWER MEDIAN PRICE WITH STRONG RATINGS =====")
print(
    eligible_groups.loc[
        eligible_groups["mean_rating"] >= 90
    ]
    .sort_values(
        ["median_price", "percent_rated_90_plus"],
        ascending=[True, False]
    )
    .head(15)
    .round(2)
    .to_string(index=False)
)

print(f"\nFull results saved to: {OUTPUT_PATH}")
print("\nAnalysis completed. Source datasets were not modified.")
