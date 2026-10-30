from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
RAW_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

# Load the original dataset
original = pd.read_csv(RAW_PATH)

# Apply the same basic cleaning rules in memory for a fair comparison
# The original CSV is not changed.
if "Unnamed: 0" in original.columns:
    original = original.drop(columns=["Unnamed: 0"])

text_columns = original.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    original[column] = original[column].str.strip()

# Create a comparison version by removing exact duplicate records
deduplicated = original.drop_duplicates().copy()

print("\n===== RECORD COUNT COMPARISON =====")
print(f"All cleaned records: {len(original):,}")
print(f"Records after deduplication: {len(deduplicated):,}")
print(f"Rows removed: {len(original) - len(deduplicated):,}")
print(
    f"Percentage of rows removed: "
    f"{(len(original) - len(deduplicated)) / len(original) * 100:.2f}%"
)

# Compare numerical statistics before and after deduplication
print("\n===== PRICE AND RATING COMPARISON =====")

for label, data in [
    ("BEFORE DEDUPLICATION", original),
    ("AFTER DEDUPLICATION", deduplicated),
]:
    print(f"\n--- {label} ---")
    print(f"Available prices: {data['price'].notna().sum():,}")
    print(f"Missing prices: {data['price'].isna().sum():,}")
    print(f"Mean price: {data['price'].mean():.2f}")
    print(f"Median price: {data['price'].median():.2f}")
    print(f"Mean rating: {data['points'].mean():.2f}")
    print(f"Median rating: {data['points'].median():.2f}")

# Compare the most frequently represented countries and varieties
for column in ["country", "variety"]:
    print(f"\n===== TOP 10 {column.upper()} COUNTS =====")

    before_counts = original[column].value_counts().head(10)
    after_counts = deduplicated[column].value_counts().head(10)

    comparison = pd.concat(
        [
            before_counts.rename("before"),
            after_counts.rename("after"),
        ],
        axis=1,
    ).fillna(0).astype(int)

    comparison["difference"] = (
        comparison["after"] - comparison["before"]
    )

    print(comparison.to_string())

print("\nDeduplication impact comparison completed.")
print("No files were overwritten or modified.")
