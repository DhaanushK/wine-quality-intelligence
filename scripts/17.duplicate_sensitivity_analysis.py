
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")

DATASETS = {
    "All cleaned records": (
        PROJECT_DIR / "data" / "processed" / "wine_reviews_cleaned.csv"
    ),
    "Deduplicated records": (
        PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
    ),
}

PRICE_LIMIT = 30
RATING_LIMIT = 90
MIN_GROUP_SIZE = 20

results = []

for dataset_name, path in DATASETS.items():
    df = pd.read_csv(path)

    # Use the same eligibility criteria for both datasets
    candidates = df.loc[
        df["price"].notna()
        & (df["price"] > 0)
        & (df["price"] <= PRICE_LIMIT)
        & df["points"].notna()
        & (df["points"] >= RATING_LIMIT)
        & df["country"].notna()
        & df["variety"].notna()
    ].copy()

    summary = (
        candidates.groupby(["country", "variety"])
        .agg(
            record_count=("points", "size"),
            mean_price=("price", "mean"),
            median_price=("price", "median"),
            mean_rating=("points", "mean"),
        )
        .reset_index()
    )

    summary = summary.loc[
        summary["record_count"] >= MIN_GROUP_SIZE
    ].copy()

    summary["dataset"] = dataset_name
    results.append(summary)

    print(f"\n===== {dataset_name.upper()} =====")
    print(f"Eligible records: {len(candidates):,}")
    print(f"Country-variety groups with at least 20 records: {len(summary):,}")

combined = pd.concat(results, ignore_index=True)

# Compare metrics for combinations meeting the minimum count
# in both datasets.
comparison = combined.pivot(
    index=["country", "variety"],
    columns="dataset",
    values=["record_count", "mean_price", "mean_rating"],
)

comparison.columns = [
    f"{metric}_{dataset}"
    for metric, dataset in comparison.columns
]
comparison = comparison.dropna().reset_index()

comparison["record_count_difference"] = (
    comparison["record_count_All cleaned records"]
    - comparison["record_count_Deduplicated records"]
)

comparison["mean_rating_difference"] = (
    comparison["mean_rating_All cleaned records"]
    - comparison["mean_rating_Deduplicated records"]
)

comparison["mean_price_difference"] = (
    comparison["mean_price_All cleaned records"]
    - comparison["mean_price_Deduplicated records"]
)

print("\n===== COMPARISON: COMBINATIONS PRESENT IN BOTH =====")
print(f"Comparable combinations: {len(comparison):,}")

print("\n===== US RIESLING AND PORTUGUESE RED =====")

focus = comparison.loc[
    (
        (comparison["country"] == "US")
        & (comparison["variety"] == "Riesling")
    )
    | (
        (comparison["country"] == "Portugal")
        & (comparison["variety"] == "Portuguese Red")
    )
]

if focus.empty:
    print("One or both combinations did not meet the comparison criteria.")
else:
    print(focus.round(2).to_string(index=False))

print("\n===== LARGEST RATING DIFFERENCES =====")
print(
    comparison.assign(
        absolute_rating_difference=lambda x: x["mean_rating_difference"].abs()
    )
    .sort_values("absolute_rating_difference", ascending=False)
    .head(10)
    .round(2)
    .to_string(index=False)
)

print("\nSensitivity analysis completed. No dataset files were modified.")
