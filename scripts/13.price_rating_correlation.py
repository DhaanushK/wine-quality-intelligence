from pathlib import Path
import pandas as pd

# Load the deduplicated dataset
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")
DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)

df = pd.read_csv(DATA_PATH)

# Correlation requires both a price and a rating
analysis_df = df.loc[
    df["price"].notna() & df["points"].notna(),
    ["price", "points"]
].copy()

print("\n===== PRICE-RATING CORRELATION =====")
print(f"Records included: {len(analysis_df):,}")

# Pearson measures linear association
pearson_corr = analysis_df["price"].corr(
    analysis_df["points"],
    method="pearson"
)

# Spearman measures monotonic association using ranks
spearman_corr = analysis_df["price"].corr(
    analysis_df["points"],
    method="spearman"
)

print(f"Pearson correlation: {pearson_corr:.4f}")
print(f"Spearman correlation: {spearman_corr:.4f}")

print("\n===== INTERPRETATION GUIDE =====")
print("Positive value: higher prices tend to accompany higher ratings.")
print("Negative value: higher prices tend to accompany lower ratings.")
print("Value near zero: little overall association by that measure.")

print("\nCorrelation analysis completed. No files were modified.")
