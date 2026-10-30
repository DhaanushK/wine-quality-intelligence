
# Step 21: Price outlier sensitivity analysis
# Compare price-rating correlations before and after
# excluding records above the overall 99th-percentile price.

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "wine_reviews_deduplicated.csv"
)

OUTPUT_FILE = (
    PROJECT_DIR
    / "reports"
    / "price_outlier_sensitivity.csv"
)

# --------------------------------------------------
# 2. Load and prepare the dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["points"] = pd.to_numeric(df["points"], errors="coerce")

df = df.dropna(
    subset=["price", "points", "country", "variety"]
).copy()

df = df[df["price"] > 0].copy()

print("=" * 70)
print("PRICE OUTLIER SENSITIVITY ANALYSIS")
print("=" * 70)

print(f"\nValid records before sensitivity filtering: {len(df):,}")

# --------------------------------------------------
# 3. Calculate the overall 99th-percentile price
# --------------------------------------------------

price_threshold = df["price"].quantile(0.99)

print(f"99th-percentile price threshold: ${price_threshold:.2f}")

# Keep all records in the full dataset.
full_df = df.copy()

# Create a separate sensitivity dataset.
# This does not modify the original CSV.
filtered_df = df[df["price"] <= price_threshold].copy()

print(f"Full dataset records: {len(full_df):,}")
print(f"Price-filtered records: {len(filtered_df):,}")
print(f"Records excluded from sensitivity analysis: "
      f"{len(full_df) - len(filtered_df):,}")

# --------------------------------------------------
# 4. Define a function to calculate correlations
# --------------------------------------------------

MIN_RECORDS = 50


def calculate_correlations(data, dataset_label):

    results = []

    grouped = data.groupby(
        ["country", "variety"],
        observed=True
    )

    for (country, variety), group in grouped:

        if len(group) < MIN_RECORDS:
            continue

        # Correlation requires variation in both variables.
        if (
            group["price"].nunique() < 2
            or group["points"].nunique() < 2
        ):
            continue

        results.append({
            "country": country,
            "variety": variety,
            "dataset": dataset_label,
            "record_count": len(group),
            "pearson_correlation": group["price"].corr(
                group["points"],
                method="pearson"
            ),
            "spearman_correlation": group["price"].corr(
                group["points"],
                method="spearman"
            )
        })

    return pd.DataFrame(results)


# --------------------------------------------------
# 5. Calculate correlations for both datasets
# --------------------------------------------------

full_results = calculate_correlations(
    full_df,
    "Full dataset"
)

filtered_results = calculate_correlations(
    filtered_df,
    "Price-filtered dataset"
)

# Match the same country-variety combinations so we
# compare like with like.
comparison = full_results.merge(
    filtered_results,
    on=["country", "variety"],
    how="inner",
    suffixes=("_full", "_filtered")
)

if comparison.empty:
    raise ValueError(
        "No country-variety combinations qualified in both datasets."
    )

# Calculate changes in correlations.
comparison["pearson_change"] = (
    comparison["pearson_correlation_filtered"]
    - comparison["pearson_correlation_full"]
)

comparison["spearman_change"] = (
    comparison["spearman_correlation_filtered"]
    - comparison["spearman_correlation_full"]
)

comparison["record_count_change"] = (
    comparison["record_count_filtered"]
    - comparison["record_count_full"]
)

comparison["abs_spearman_change"] = (
    comparison["spearman_change"].abs()
)

# --------------------------------------------------
# 6. Save the comparison report
# --------------------------------------------------

comparison.to_csv(OUTPUT_FILE, index=False)

print(f"\nCountry-variety combinations in full dataset: "
      f"{len(full_results):,}")

print(f"Country-variety combinations in filtered dataset: "
      f"{len(filtered_results):,}")

print(f"Comparable combinations: {len(comparison):,}")

print(f"\nReport saved to:\n{OUTPUT_FILE}")

# --------------------------------------------------
# 7. Summarise the impact
# --------------------------------------------------

print("\nAVERAGE CORRELATION COMPARISON")

print(
    f"Mean Pearson correlation, full: "
    f"{comparison['pearson_correlation_full'].mean():.4f}"
)

print(
    f"Mean Pearson correlation, filtered: "
    f"{comparison['pearson_correlation_filtered'].mean():.4f}"
)

print(
    f"Mean Spearman correlation, full: "
    f"{comparison['spearman_correlation_full'].mean():.4f}"
)

print(
    f"Mean Spearman correlation, filtered: "
    f"{comparison['spearman_correlation_filtered'].mean():.4f}"
)

print(
    f"Median absolute Spearman change: "
    f"{comparison['abs_spearman_change'].median():.4f}"
)

# --------------------------------------------------
# 8. Show the combinations with the biggest changes
# --------------------------------------------------

display_columns = [
    "country",
    "variety",
    "record_count_full",
    "record_count_filtered",
    "spearman_correlation_full",
    "spearman_correlation_filtered",
    "spearman_change"
]

print("\nTOP 10 LARGEST ABSOLUTE SPEARMAN CHANGES")

print(
    comparison.nlargest(10, "abs_spearman_change")[
        display_columns
    ].round(4).to_string(index=False)
)

print("\nTOP 10 LARGEST ABSOLUTE PEARSON CHANGES")

comparison["abs_pearson_change"] = (
    comparison["pearson_change"].abs()
)

print(
    comparison.nlargest(10, "abs_pearson_change")[
        [
            "country",
            "variety",
            "record_count_full",
            "record_count_filtered",
            "pearson_correlation_full",
            "pearson_correlation_filtered",
            "pearson_change"
        ]
    ].round(4).to_string(index=False)
)

print("\n" + "=" * 70)
print("SENSITIVITY ANALYSIS COMPLETED")
print("=" * 70)
