from pathlib import Path
import pandas as pd

# Locate and load the original dataset
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "winemag-data_first150k.csv"

df = pd.read_csv(DATASET_PATH)

# Select available prices without changing the original data
prices = df["price"].dropna()

print("\n===== PRICE QUALITY AUDIT =====")
print(f"Total records: {len(df):,}")
print(f"Missing prices: {df['price'].isna().sum():,}")
print(f"Available prices: {len(prices):,}")

# Inspect the price distribution
print("\n===== PRICE PERCENTILES =====")
print(
    prices.describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    ).to_string()
)

# Calculate the interquartile range (IQR)
# IQR measures the spread of the middle 50% of prices.
q1 = prices.quantile(0.25)
q3 = prices.quantile(0.75)
iqr = q3 - q1

# Calculate conventional statistical outlier boundaries
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print("\n===== IQR OUTLIER INVESTIGATION =====")
print(f"First quartile (Q1): {q1:.2f}")
print(f"Third quartile (Q3): {q3:.2f}")
print(f"Interquartile range (IQR): {iqr:.2f}")
print(f"Lower boundary: {lower_bound:.2f}")
print(f"Upper boundary: {upper_bound:.2f}")

# Count prices outside the statistical boundaries
outlier_mask = (prices < lower_bound) | (prices > upper_bound)

print(f"Potential statistical outliers: {outlier_mask.sum():,}")
print(f"Potential outlier percentage: {outlier_mask.mean() * 100:.2f}%")

# Display the 10 highest listed prices for investigation
print("\n===== TEN HIGHEST LISTED PRICES =====")
print(
    df.loc[df["price"].notna(), ["country", "points", "price", "variety", "winery"]]
    .nlargest(10, "price")
    .to_string(index=False)
)

print("\nPrice quality audit completed. No records were modified.")
