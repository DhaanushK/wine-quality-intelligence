from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Define paths
PROJECT_DIR = Path(r"D:\Masters in AI\Wine Business Intelligence Project")

DATA_PATH = (
    PROJECT_DIR / "data" / "processed" / "wine_reviews_deduplicated.csv"
)
FIGURES_DIR = PROJECT_DIR / "reports" / "figures"

# Create the output directory if it does not exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Load the deduplicated analytical dataset
df = pd.read_csv(DATA_PATH)

# Select records with valid prices for price-related charts
priced = df.loc[df["price"].notna() & (df["price"] > 0)].copy()

print(f"Total records: {len(df):,}")
print(f"Records with valid prices: {len(priced):,}")

# --------------------------------------------------
# CHART 1: PRICE DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(priced["price"], bins=50, edgecolor="black")

# Limit the displayed range so the main distribution is visible.
# The data itself is not removed or modified.
price_display_limit = priced["price"].quantile(0.99)
plt.xlim(0, price_display_limit)

plt.title("Distribution of Wine Prices (Up to 99th Percentile)")
plt.xlabel("Listed Price")
plt.ylabel("Number of Records")
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "01_price_distribution.png",
    dpi=300
)
plt.show()
plt.close()

# --------------------------------------------------
# CHART 2: CRITIC RATING DISTRIBUTION
# --------------------------------------------------

rating_counts = df["points"].value_counts().sort_index()

plt.figure(figsize=(10, 6))

plt.bar(
    rating_counts.index,
    rating_counts.values,
    edgecolor="black"
)

plt.title("Distribution of Wine Critic Ratings")
plt.xlabel("Critic Rating (Points)")
plt.ylabel("Number of Records")
plt.xticks(range(80, 101, 2))
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "02_rating_distribution.png",
    dpi=300
)
plt.show()
plt.close()

# --------------------------------------------------
# CHART 3: PRICE VERSUS CRITIC RATING
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    priced["price"],
    priced["points"],
    alpha=0.15,
    s=12
)

# A logarithmic axis makes the broad price range easier to inspect.
plt.xscale("log")

plt.title("Wine Price versus Critic Rating")
plt.xlabel("Listed Price (Logarithmic Scale)")
plt.ylabel("Critic Rating (Points)")
plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "03_price_vs_rating.png",
    dpi=300
)
plt.show()
plt.close()

print("\n===== VISUALIZATIONS SAVED =====")

for filename in [
    "01_price_distribution.png",
    "02_rating_distribution.png",
    "03_price_vs_rating.png",
]:
    print(FIGURES_DIR / filename)

print("\nEDA visualization step completed.")
