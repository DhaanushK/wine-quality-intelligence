
import csv
from decimal import Decimal
from getpass import getpass
from pathlib import Path

import mysql.connector

# --------------------------------------------------
# 1. File and database configuration
# --------------------------------------------------

CSV_PATH = Path(
    r"data\processed\wine_reviews_deduplicated.csv"
)

EXPECTED_ROWS = 97851
EXPECTED_COLUMNS = 10
EXPECTED_BLANK_PRICES = 8720
BATCH_SIZE = 500

COLUMNS = [
    "country",
    "description",
    "designation",
    "points",
    "price",
    "province",
    "region_1",
    "region_2",
    "variety",
    "winery",
]


def main():
    # --------------------------------------------------
    # 2. Validate the complete CSV before touching MySQL
    # --------------------------------------------------

    rows_to_import = []
    blank_prices = 0

    print("Reading and validating the source CSV...")

    with CSV_PATH.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != COLUMNS:
            raise ValueError(
                f"Unexpected CSV columns: {reader.fieldnames}"
            )

        for line_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(
                    f"Invalid record structure at CSV line {line_number}"
                )

            # Convert empty fields into Python None.
            # MySQL Connector sends None as SQL NULL.
            cleaned = {
                key: (value if value.strip() != "" else None)
                for key, value in row.items()
            }

            # Validate and convert numeric fields.
            points = int(cleaned["points"])

            if cleaned["price"] is None:
                price = None
                blank_prices += 1
            else:
                price = Decimal(cleaned["price"])

            values = tuple(
                points if column == "points"
                else price if column == "price"
                else cleaned[column]
                for column in COLUMNS
            )

            rows_to_import.append(values)

    if len(rows_to_import) != EXPECTED_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_ROWS} rows, "
            f"found {len(rows_to_import)}. Import cancelled."
        )

    if blank_prices != EXPECTED_BLANK_PRICES:
        raise ValueError(
            f"Expected {EXPECTED_BLANK_PRICES} blank prices, "
            f"found {blank_prices}. Import cancelled."
        )

    print(f"CSV rows validated: {len(rows_to_import):,}")
    print(f"Blank prices to store as NULL: {blank_prices:,}")
    print("CSV validation passed.")

    # --------------------------------------------------
    # 3. Connect to MySQL
    # --------------------------------------------------

    password = getpass("Enter your MySQL password: ")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="wine_quality_intelligence",
        charset="utf8mb4",
    )

    cursor = connection.cursor()

    try:
        # Confirm the destination table has the expected columns.
        cursor.execute("SHOW COLUMNS FROM wine_reviews")
        table_columns = [row[0] for row in cursor.fetchall()]

        expected_table_columns = ["review_id"] + COLUMNS

        if table_columns != expected_table_columns:
            raise ValueError(
                "The MySQL table structure does not match "
                "the expected 11 columns. No rows were replaced."
            )

        # --------------------------------------------------
        # 4. Replace the existing import in one transaction
        # --------------------------------------------------

        insert_sql = """
            INSERT INTO wine_reviews (
                country, description, designation, points, price,
                province, region_1, region_2, variety, winery
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        print("\nStarting database transaction...")

        # Remove the incorrect import only after validation
        # and connection/table checks have succeeded.
        cursor.execute("DELETE FROM wine_reviews")

        inserted = 0

        for start in range(0, len(rows_to_import), BATCH_SIZE):
            batch = rows_to_import[start:start + BATCH_SIZE]

            cursor.executemany(insert_sql, batch)
            inserted += len(batch)

            print(
                f"Prepared {inserted:,} / "
                f"{len(rows_to_import):,} rows"
            )

        # Verify counts before committing.
        cursor.execute("SELECT COUNT(*) FROM wine_reviews")
        actual_rows = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM wine_reviews WHERE price IS NULL"
        )
        actual_missing_prices = cursor.fetchone()[0]

        if actual_rows != EXPECTED_ROWS:
            raise ValueError(
                f"Row-count mismatch: {actual_rows}"
            )

        if actual_missing_prices != EXPECTED_BLANK_PRICES:
            raise ValueError(
                f"Missing-price mismatch: {actual_missing_prices}"
            )

        connection.commit()

        print("\nIMPORT SUCCESSFUL")
        print(f"Rows imported: {actual_rows:,}")
        print(f"NULL prices: {actual_missing_prices:,}")
        print("Changes committed to MySQL.")

    except Exception:
        connection.rollback()
        print(
            "\nIMPORT FAILED. The transaction was rolled back "
            "where supported by the table's storage engine."
        )
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
