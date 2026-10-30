
import csv
from pathlib import Path

# Path to the original deduplicated dataset
file_path = Path(
    r"data\processed\wine_reviews_deduplicated.csv"
)

expected_columns = 10
total_records = 0
incorrect_rows = []
blank_prices = 0

with file_path.open(
    mode="r",
    encoding="utf-8-sig",
    newline=""
) as file:

    reader = csv.reader(file)

    # Read the header separately
    header = next(reader)

    print("CSV HEADER:")
    print(header)
    print("\nExpected columns:", expected_columns)
    print("Actual columns:", len(header))

    # Validate each data record
    for line_number, row in enumerate(reader, start=2):
        total_records += 1

        if len(row) != expected_columns:
            incorrect_rows.append(
                (line_number, len(row), row[:3])
            )

        # Price is the fifth column (index 4)
        if len(row) == expected_columns and row[4].strip() == "":
            blank_prices += 1

print("\nCSV VALIDATION RESULTS")
print("-" * 40)
print("Total data records:", total_records)
print("Rows with blank prices:", blank_prices)
print("Rows with incorrect column counts:", len(incorrect_rows))

if incorrect_rows:
    print("\nFirst 10 problematic records:")
    for record in incorrect_rows[:10]:
        print(record)

if (
    total_records == 97851
    and len(header) == expected_columns
    and not incorrect_rows
):
    print("\nPASS: CSV structure is valid.")
else:
    print("\nCHECK REQUIRED: CSV structure differs from expectations.")
