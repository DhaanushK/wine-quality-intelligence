
# Step 20: Visualise country-variety price-rating correlations

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "reports"
    / "country_variety_correlation.csv"
)

FIGURES_DIR = PROJECT_DIR / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Load correlation results
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "country",
    "variety",
    "record_count",
    "spearman_correlation",
    "pearson_correlation"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

df = df.dropna(
    subset=["country", "variety", "spearman_correlation"]
).copy()

# Create readable labels for the charts.
df["country_variety"] = (
    df["country"].astype(str)
    + " — "
    + df["variety"].astype(str)
)

# --------------------------------------------------
# 3. Chart 1: Strongest positive Spearman correlations
# --------------------------------------------------

strongest = (
    df.nlargest(15, "spearman_correlation")
    .sort_values("spearman_correlation")
)

fig, ax = plt.subplots(figsize=(12, 8))

ax.barh(
    strongest["country_variety"],
    strongest["spearman_correlation"]
)

ax.set_title(
    "Strongest Price–Rating Relationships by Country and Variety"
)
ax.set_xlabel("Spearman Correlation")
ax.set_ylabel("Country — Variety")
ax.set_xlim(-1, 1)
ax.axvline(0, linewidth=1)
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()

strongest_path = (
    FIGURES_DIR
    / "04_strongest_country_variety_correlations.png"
)

fig.savefig(strongest_path, dpi=300, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------
# 4. Chart 2: Weakest Spearman correlations
# --------------------------------------------------

weakest = (
    df.nsmallest(15, "spearman_correlation")
    .sort_values("spearman_correlation")
)

fig, ax = plt.subplots(figsize=(12, 8))

ax.barh(
    weakest["country_variety"],
    weakest["spearman_correlation"]
)

ax.set_title(
    "Weakest Price–Rating Relationships by Country and Variety"
)
ax.set_xlabel("Spearman Correlation")
ax.set_ylabel("Country — Variety")
ax.set_xlim(-1, 1)
ax.axvline(0, linewidth=1)
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()

weakest_path = (
    FIGURES_DIR
    / "05_weakest_country_variety_correlations.png"
)

fig.savefig(weakest_path, dpi=300, bbox_inches="tight")
plt.close(fig)

# --------------------------------------------------
# 5. Report completion
# --------------------------------------------------

print("=" * 65)
print("COUNTRY–VARIETY CORRELATION VISUALISATION")
print("=" * 65)

print(f"\nCombinations visualised: {len(df):,}")

print("\nChart 1 saved:")
print(strongest_path)

print("\nChart 2 saved:")
print(weakest_path)

print("\nBoth charts use Spearman correlation.")
print("A value near +1 indicates a strong positive association.")
print("A value near -1 indicates a strong negative association.")
print("A value near 0 indicates a weak monotonic association.")

print("\nVisualisation completed successfully.")
