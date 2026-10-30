from pathlib import Path
import pandas as pd

# Load the original dataset without modifying it
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

df = pd.read_csv(DATASET_PATH)

print("\n===== MISSING GEOGRAPHICAL INFORMATION =====")

# Inspect rows where country or province is missing
missing_geo = df.loc[
    df["country"].isna() | df["province"].isna(),
    ["country", "province", "region_1", "region_2", "variety", "winery"]
]

print(f"Rows with missing country or province: {len(missing_geo):,}")
print(missing_geo.to_string(index=False))

print("\n===== DISTINCT CATEGORY COUNTS =====")

# Count distinct non-missing values in important text columns
categorical_columns = [
    "country",
    "province",
    "region_1",
    "region_2",
    "variety",
    "winery"
]

for column in categorical_columns:
    print(f"{column}: {df[column].nunique(dropna=True):,} distinct values")

print("\n===== LEADING OR TRAILING WHITESPACE =====")

# Identify text values that contain unnecessary spaces
for column in categorical_columns:
    text_values = df[column].dropna().astype("string")
    whitespace_mask = text_values.ne(text_values.str.strip())

    print(f"{column}: {whitespace_mask.sum():,} values with extra outer spaces")

print("\n===== COUNTRY CAPITALIZATION CHECK =====")

# Compare original country labels with their lowercase versions
countries = df["country"].dropna().astype("string")

country_case_check = pd.DataFrame({
    "original": countries,
    "lowercase": countries.str.lower()
}).drop_duplicates()

case_groups = (
    country_case_check.groupby("lowercase")["original"]
    .agg(list)
)

inconsistent_case = case_groups[case_groups.map(len) > 1]

if inconsistent_case.empty:
    print("No country labels differing only by capitalization were found.")
else:
    print("Country labels that differ only by capitalization:")
    for labels in inconsistent_case:
        print(labels)

print("\nCategorical quality audit completed. No records were modified.")
