from pathlib import Path
import pandas as pd

# Define the project directory and dataset paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")

CLEAN_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_cleaned.csv"
)
DEDUP_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)

# Load both datasets for comparison
cleaned = pd.read_csv(CLEAN_PATH)
deduplicated = pd.read_csv(DEDUP_PATH)

# Display a high-level comparison
print("\n===== DATASET OVERVIEW =====")

for name, data in [
    ("ALL CLEANED RECORDS", cleaned),
    ("DEDUPLICATED RECORDS", deduplicated),
]:
    print(f"\n--- {name} ---")
    print(f"Rows: {len(data):,}")
    print(f"Columns: {len(data.columns):,}")
    print(f"Countries: {data['country'].nunique():,}")
    print(f"Wine varieties: {data['variety'].nunique():,}")
    print(f"Wineries: {data['winery'].nunique():,}")
    print(f"Missing country values: {data['country'].isna().sum():,}")
    print(f"Missing variety values: {data['variety'].isna().sum():,}")
    print(f"Missing price values: {data['price'].isna().sum():,}")

# Examine the main numerical variables
print("\n===== PRICE AND RATING SUMMARY =====")

print(
    deduplicated[["price", "points"]]
    .describe(percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
    .round(2)
    .to_string()
)

# Identify countries with the most recorded wine entries
print("\n===== TOP 10 COUNTRIES BY RECORD COUNT =====")

print(
    deduplicated["country"]
    .value_counts()
    .head(10)
    .rename_axis("country")
    .reset_index(name="record_count")
    .to_string(index=False)
)

# Identify the most frequently recorded wine varieties
print("\n===== TOP 10 VARIETIES BY RECORD COUNT =====")

print(
    deduplicated["variety"]
    .value_counts()
    .head(10)
    .rename_axis("variety")
    .reset_index(name="record_count")
    .to_string(index=False)
)

# Examine the most common rating values
print("\n===== RATING DISTRIBUTION =====")

print(
    deduplicated["points"]
    .value_counts()
    .sort_index()
    .rename_axis("points")
    .reset_index(name="record_count")
    .to_string(index=False)
)

print("\nEDA overview completed. No dataset files were modified.")
