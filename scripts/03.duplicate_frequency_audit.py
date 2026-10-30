from pathlib import Path
import pandas as pd

# Define the original dataset location
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

# Load the original data without modifying it
df = pd.read_csv(DATASET_PATH)

# Exclude the sequential index from the duplicate comparison
index_column = "Unnamed: 0"

if index_column in df.columns:
    business_data = df.drop(columns=[index_column])
else:
    business_data = df.copy()

# Count how many times each distinct record occurs
record_counts = business_data.value_counts(dropna=False)

# Keep only records that occur more than once
duplicate_groups = record_counts[record_counts > 1]

# Calculate the number of extra occurrences
extra_occurrences = (duplicate_groups - 1).sum()

print("\n===== DUPLICATE FREQUENCY AUDIT =====")
print(f"Total original records: {len(df):,}")
print(f"Distinct record combinations: {len(record_counts):,}")
print(f"Repeated record groups: {len(duplicate_groups):,}")
print(f"Rows in repeated groups: {duplicate_groups.sum():,}")
print(f"Extra occurrences beyond the first: {extra_occurrences:,}")

if not duplicate_groups.empty:
    print(
        "Maximum occurrences of one record:",
        int(duplicate_groups.max())
    )

    # Count how many duplicate groups have each repetition frequency
    frequency_distribution = (
        duplicate_groups.value_counts()
        .sort_index()
        .rename_axis("Occurrences_Per_Record")
        .reset_index(name="Number_of_Record_Groups")
    )

    print("\n===== REPETITION FREQUENCY DISTRIBUTION =====")
    print(frequency_distribution.to_string(index=False))

    # Show the ten most frequently occurring records
    print("\n===== TEN MOST FREQUENTLY REPEATED RECORDS =====")

    top_records = (
        duplicate_groups
        .sort_values(ascending=False)
        .head(10)
        .rename("Occurrences")
        .reset_index()
    )

    print(top_records.to_string(index=False))

else:
    print("No repeated record groups were found.")

print("\nDuplicate frequency audit completed.")
