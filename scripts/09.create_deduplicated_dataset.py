from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")

CLEAN_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_cleaned.csv"
)
OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)

# Load the cleaned dataset; do not change the existing file
df = pd.read_csv(CLEAN_PATH)

# Remove exact duplicate rows, keeping the first occurrence
deduplicated = df.drop_duplicates().copy()

# Save the result as a separate analytical dataset
deduplicated.to_csv(OUTPUT_PATH, index=False)

print("\n===== DEDUPLICATED DATASET CREATED =====")
print(f"Input records: {len(df):,}")
print(f"Output records: {len(deduplicated):,}")
print(f"Rows removed: {len(df) - len(deduplicated):,}")
print(f"Duplicate rows remaining: {deduplicated.duplicated().sum():,}")
print(f"Saved to: {OUTPUT_PATH}")

print("\nOriginal and cleaned datasets were not overwritten.")
