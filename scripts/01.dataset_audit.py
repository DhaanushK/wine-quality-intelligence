from pathlib import Path
import pandas as pd

# 1. Define the project and dataset locations
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

# 2. Verify that the dataset exists
if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATASET_PATH}\n"
        "Check the filename and the data\\raw folder."
    )

# 3. Load the CSV into a Pandas DataFrame
# A DataFrame is a table of rows and columns, like a spreadsheet.
df = pd.read_csv(DATASET_PATH)

# 4. Inspect the dataset dimensions
print("\n===== DATASET DIMENSIONS =====")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

# 5. Inspect the column names
print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

# 6. Inspect data types and non-missing counts
print("\n===== DATA TYPES AND NON-MISSING COUNTS =====")
df.info()

# 7. Count missing values and calculate their percentages
print("\n===== MISSING VALUE AUDIT =====")
missing_report = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percentage": (df.isna().mean() * 100).round(2)
})

print(
    missing_report
    .sort_values("Missing_Percentage", ascending=False)
    .to_string()
)

# 8. Count exact duplicate rows
print("\n===== EXACT DUPLICATE ROWS =====")
print(df.duplicated().sum())

# 9. Inspect numerical columns
print("\n===== NUMERICAL SUMMARY =====")
print(df.describe().T.to_string())

# 10. Inspect price and critic-rating ranges
for column in ["price", "points"]:
    if column in df.columns:
        print(f"\n===== {column.upper()} DISTRIBUTION =====")
        print(
            df[column]
            .describe(percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
            .to_string()
        )

print("\nInitial dataset audit completed.")
