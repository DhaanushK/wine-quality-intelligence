from pathlib import Path
import pandas as pd

# Load the deduplicated analytical dataset
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)

df = pd.read_csv(DATA_PATH)

# Keep records with valid prices and critic ratings
analysis_df = df.loc[
    df["price"].notna()
    & (df["price"] > 0)
    & df["points"].notna()
].copy()

# Define price ranges
bins = [0, 15, 30, 50, 100, float("inf")]
labels = ["Up to $15", "$15–30", "$30–50", "$50–100", "Over $100"]

analysis_df["price_band"] = pd.cut(
    analysis_df["price"],
    bins=bins,
    labels=labels,
    include_lowest=True,
    right=True
)

# Calculate rating and record-count metrics by price band
summary = (
    analysis_df.groupby("price_band", observed=False)
    .agg(
        record_count=("points", "size"),
        mean_price=("price", "mean"),
        median_price=("price", "median"),
        mean_rating=("points", "mean"),
        median_rating=("points", "median"),
        highest_rating=("points", "max"),
        wines_rated_90_or_higher=("points", lambda s: (s >= 90).sum())
    )
    .reset_index()
)

# Calculate the share of records rated 90 points or higher
summary["percent_rated_90_plus"] = (
    summary["wines_rated_90_or_higher"]
    / summary["record_count"]
    * 100
)

print("\n===== PRICE BAND ANALYSIS =====")
print(
    summary.round(2).to_string(index=False)
)

print("\n===== BUSINESS INTERPRETATION CHECK =====")
print(
    "Compare the mean and median ratings across price bands. "
    "Also compare the percentage rated 90+ and the number of records "
    "in each band."
)

print("\nPrice band analysis completed. No files were modified.")
