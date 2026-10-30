from pathlib import Path
import pandas as pd

# Define the project and source dataset paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

# Load the original dataset without modifying it
df = pd.read_csv(DATASET_PATH)

# Check whether the potential index column exists
index_column = "Unnamed: 0"

print("\n===== INDEX COLUMN INVESTIGATION =====")

if index_column in df.columns:
    index_values = df[index_column]

    # Check whether the values are sequential from 0 to row_count - 1
    expected_index = pd.Series(range(len(df)))

    is_sequential = index_values.reset_index(drop=True).equals(
        expected_index
    )

    print(f"Index column found: {index_column}")
    print(f"Unique index values: {index_values.nunique(dropna=False):,}")
    print(f"Sequential from 0: {is_sequential}")
else:
    print("Potential index column was not found.")

# Check duplicates after excluding the potential index column
print("\n===== DUPLICATE INVESTIGATION =====")

if index_column in df.columns:
    business_columns = df.drop(columns=[index_column])
else:
    business_columns = df.copy()

duplicate_mask = business_columns.duplicated(keep=False)

print(
    "Rows belonging to duplicate groups, excluding the index:",
    f"{duplicate_mask.sum():,}"
)

print(
    "Repeated rows beyond the first occurrence in each group:",
    f"{business_columns.duplicated().sum():,}"
)

# Display a small sample for manual investigation
duplicate_samples = business_columns.loc[duplicate_mask].head(10)

print("\n===== SAMPLE OF POTENTIAL DUPLICATE RECORDS =====")

if duplicate_samples.empty:
    print("No duplicate records found after excluding the index.")
else:
    print(duplicate_samples.to_string(index=False))

print("\nIndex and duplicate investigation completed.")
