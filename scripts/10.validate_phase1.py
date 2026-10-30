from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")

files = {
    "Original": PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv",
    "Cleaned": PROJECT_DIR / "data" / "processed" / "wine_reviews_cleaned.csv",
    "Deduplicated": PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv",
}

expected_rows = {
    "Original": 150930,
    "Cleaned": 150930,
    "Deduplicated": 97851,
}

print("\n===== PHASE 1 VALIDATION =====")

for label, path in files.items():
    print(f"\n--- {label} dataset ---")

    if not path.exists():
        print(f"ERROR: File not found: {path}")
        continue

    df = pd.read_csv(path)

    print(f"File exists: Yes")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Missing prices: {df['price'].isna().sum():,}")
    print(f"Exact duplicate rows: {df.duplicated().sum():,}")

    if len(df) == expected_rows[label]:
        print("Row count check: PASS")
    else:
        print(
            f"Row count check: REVIEW "
            f"(expected {expected_rows[label]:,})"
        )

    if label == "Original":
        print(
            "Source index column present: "
            f"{'Unnamed: 0' in df.columns}"
        )
    else:
        print(
            "Source index column absent: "
            f"{'Unnamed: 0' not in df.columns}"
        )

print("\nValidation report completed.")
