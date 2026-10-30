from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
RAW_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"
OUTPUT_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_cleaned.csv"
)

# Load the original data
df = pd.read_csv(RAW_PATH)

original_rows = len(df)
original_columns = len(df.columns)

print("\n===== INITIAL CLEANING =====")
print(f"Original rows: {original_rows:,}")
print(f"Original columns: {original_columns:,}")

# Remove the sequential source index from analytical columns
# This field identifies row position, not a meaningful wine attribute.
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])
    print("Removed source index column: Unnamed: 0")
else:
    print("Source index column was not present.")

# Standardize outer whitespace in text columns.
# Missing values remain missing.
text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Do not fill missing values or remove duplicate records yet.
# Those decisions will be evaluated separately.
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("\n===== CLEANED DATASET SUMMARY =====")
print(f"Rows retained: {len(df):,}")
print(f"Columns retained: {len(df.columns):,}")
print(f"Missing prices: {df['price'].isna().sum():,}")
print(f"Exact duplicate rows in cleaned file: {df.duplicated().sum():,}")
print(f"Saved to: {OUTPUT_PATH}")

print("\nInitial cleaning completed. Original dataset was not modified.")
