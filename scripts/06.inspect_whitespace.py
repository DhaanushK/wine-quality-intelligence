from pathlib import Path
import pandas as pd

# Load the original dataset
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

df = pd.read_csv(DATASET_PATH)

columns_to_check = ["region_1", "variety", "winery"]

print("\n===== WHITESPACE VALUE INSPECTION =====")

for column in columns_to_check:
    values = df[column].dropna().astype("string")

    # Find values that change when outer spaces are removed
    mask = values.ne(values.str.strip())
    affected_values = values[mask]

    print(f"\n--- {column} ---")
    print(f"Rows affected: {len(affected_values):,}")

    if affected_values.empty:
        print("No affected values found.")
        continue

    # Display original and proposed cleaned labels with their frequencies
    comparison = pd.DataFrame({
        "original_value": affected_values,
        "trimmed_value": affected_values.str.strip()
    })

    summary = (
        comparison.groupby(
            ["original_value", "trimmed_value"],
            dropna=False
        )
        .size()
        .reset_index(name="row_count")
    )

    print(summary.to_string(index=False))

print("\nInspection completed. No records were modified.")
