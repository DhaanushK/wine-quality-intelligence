from pathlib import Path
import pandas as pd

# Define project paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)

df = pd.read_csv(DATA_PATH)

# Keep records with valid prices, ratings, and category labels
df = df.loc[
    df["price"].notna()
    & df["points"].notna()
    & df["country"].notna()
    & df["variety"].notna()
].copy()

# Define our exploratory affordability and rating thresholds
PRICE_LIMIT = 30
RATING_LIMIT = 90

candidates = df.loc[
    (df["price"] <= PRICE_LIMIT)
    & (df["points"] >= RATING_LIMIT)
].copy()

print("\n===== AFFORDABLE, HIGHLY RATED RECORDS =====")
print(f"Price threshold: <= {PRICE_LIMIT}")
print(f"Rating threshold: >= {RATING_LIMIT}")
print(f"Matching records: {len(candidates):,}")

if not candidates.empty:
    print(
        f"Percentage of eligible priced records: "
        f"{len(candidates) / len(df[df['price'].notna()]) * 100:.2f}%"
    )

    print("\n===== TOP 10 COUNTRIES =====")
    country_summary = (
        candidates.groupby("country")
        .agg(
            record_count=("points", "size"),
            mean_price=("price", "mean"),
            mean_rating=("points", "mean"),
        )
        .query("record_count >= 20")
        .sort_values("record_count", ascending=False)
        .head(10)
    )

    print(country_summary.round(2).to_string())

    print("\n===== TOP 10 VARIETIES =====")
    variety_summary = (
        candidates.groupby("variety")
        .agg(
            record_count=("points", "size"),
            mean_price=("price", "mean"),
            mean_rating=("points", "mean"),
        )
        .query("record_count >= 20")
        .sort_values("record_count", ascending=False)
        .head(10)
    )

    print(variety_summary.round(2).to_string())

    print("\n===== EXAMPLE RECORDS =====")
    print(
        candidates[
            ["country", "province", "variety", "winery", "price", "points"]
        ]
        .sort_values(
            ["points", "price"],
            ascending=[False, True]
        )
        .head(15)
        .to_string(index=False)
    )
else:
    print("No records matched the selected thresholds.")

print("\nAffordable high-rating analysis completed.")
print("No dataset files were modified.")
