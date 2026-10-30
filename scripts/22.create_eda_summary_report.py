
# Step 22: Generate the Wine Quality Intelligence EDA report

from pathlib import Path
from datetime import date
import pandas as pd

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_DIR / "reports"

OUTPUT_FILE = REPORTS_DIR / "eda_summary_report.md"

CORRELATION_FILE = (
    REPORTS_DIR / "country_variety_correlation.csv"
)

SENSITIVITY_FILE = (
    REPORTS_DIR / "price_outlier_sensitivity.csv"
)

VALUE_FILE = (
    REPORTS_DIR / "country_variety_value_analysis.csv"
)

OVERALL_FILE = (
    REPORTS_DIR / "overall_country_variety_analysis.csv"
)

# --------------------------------------------------
# 2. Check that required analysis outputs exist
# --------------------------------------------------

required_files = [
    CORRELATION_FILE,
    SENSITIVITY_FILE,
    VALUE_FILE,
    OVERALL_FILE,
]

missing_files = [
    str(path) for path in required_files
    if not path.exists()
]

if missing_files:
    raise FileNotFoundError(
        "The following analysis files are missing:\n"
        + "\n".join(missing_files)
    )

# Load existing reports to verify their availability and
# include their actual group counts in the summary.
correlations = pd.read_csv(CORRELATION_FILE)
sensitivity = pd.read_csv(SENSITIVITY_FILE)
value_analysis = pd.read_csv(VALUE_FILE)
overall_analysis = pd.read_csv(OVERALL_FILE)

# --------------------------------------------------
# 3. Define the report content
# --------------------------------------------------

report = f"""# Wine Quality Intelligence
## Exploratory Data Analysis (EDA) Summary Report

**Report generated:** {date.today().isoformat()}

**Project type:** Data Analytics and Business Intelligence

---

## 1. Executive Summary

This project analyses historical wine review data to understand
the relationships between listed prices, critic ratings, countries,
regions and wine varieties.

The analysis focuses on price distributions, rating patterns,
comparisons across country-variety segments, and the identification
of comparatively affordable wines with high critic ratings.

The dataset contains review descriptions, listed prices and critic
scores. It does not contain verified sales, profit, inventory,
consumer demand or transaction data. Findings should therefore be
interpreted as descriptive insights from review records rather than
proof of commercial performance.

## 2. Dataset Overview

The original Wine Enthusiast dataset contains 150,930 records and
11 columns.

The original sequential index column was removed from the analytical
copy because it was not a useful business feature.

Two analytical versions were retained:

- `data/processed/wine_reviews_cleaned.csv`
- `data/processed/wine_reviews_deduplicated.csv`

The cleaned version preserves all 150,930 records while removing
the source index column and trimming justified outer whitespace.

The deduplicated version contains 97,851 records after removing
53,079 repeated rows based on the remaining fields.

**Important:** Identical records are not necessarily erroneous
reviews. Because a reliable unique review identifier is unavailable,
the deduplicated dataset is used as the primary analytical version,
while the cleaned dataset is retained for sensitivity comparisons.

## 3. Data Quality and Cleaning

Key data-quality findings from the initial audit:

- Missing prices in the original dataset: 13,695.
- Missing `region_2` values: 89,977.
- Missing `designation` values: 45,735.
- Missing `region_1` values: 25,060.
- Original exact duplicate rows across all 11 columns: 0.

The original index was excluded when investigating repeated records.
Missing geographic and designation values were retained rather than
invented or inferred.

Unusually high prices were investigated but not automatically
deleted. Price-related analyses use valid positive prices where
appropriate.

## 4. Overall Price and Rating Patterns

In the deduplicated dataset:

- Total records: 97,851.
- Records with valid prices: 89,131.
- Mean price: approximately $33.66.
- Median price: $25.
- 99th-percentile price: approximately $152.70.
- Maximum recorded price: $2,300.
- Mean critic rating: approximately 87.96.
- Median critic rating: 88.

The price distribution is right-skewed: most listed prices are
substantially lower than the small number of very expensive wines.

Ratings are concentrated in the upper 80s and low 90s, with 87
being the most frequent score.

## 5. Overall Price–Rating Relationship

Using records with valid prices and ratings:

- Pearson correlation: 0.4474.
- Spearman correlation: 0.5987.

These results indicate a positive association between price and
critic rating in the analysed records. The rank-based association
is stronger than the linear association.

Correlation does not establish causation. These findings do not
prove that increasing a wine's price causes a higher rating.

## 6. Price-Band Analysis

Average ratings increased across the price bands in the analysis:

| Price band | Records | Mean rating | Percentage rated 90+ |
|---|---:|---:|---:|
| Up to $15 | 21,534 | 85.47 | 4.16% |
| Above $15 to $30 | 35,224 | 87.36 | 22.77% |
| Above $30 to $50 | 19,304 | 89.20 | 51.03% |
| Above $50 to $100 | 10,732 | 90.85 | 72.87% |
| Above $100 | 2,337 | 92.81 | 88.23% |

This descriptive pattern suggests that higher-priced wines in this
dataset tend to have higher critic ratings. It does not mean that
every expensive wine is highly rated or that affordable wines lack
quality.

## 7. Affordable, Highly Rated Wines

The project defined an affordable, highly rated wine for this
analysis as a record with:

- Listed price at or below $30.
- Critic rating of at least 90.

The deduplicated dataset contained 8,912 matching records.

Examples of country-variety combinations identified for further
investigation include:

- United States — Riesling.
- Portugal — Portuguese Red.
- United States — Chardonnay.
- United States — Sauvignon Blanc.
- Austria — Riesling.

These are candidates for further comparison, not definitive
recommendations for consumers or proof of market demand.

The analysis requires adequate group sizes to reduce the influence
of very small samples. Results may differ if the price threshold,
rating threshold or minimum group size changes.

## 8. Country–Variety Analysis

The project compared wine varieties within individual countries
rather than relying only on country-wide or global averages.

In the overall country-variety analysis, groups with at least
30 valid records were retained. Examples included:

- Italy — Sangiovese Grosso: 628 records, mean rating 90.82,
  median price $55.
- Austria — Riesling: 291 records, mean rating 90.56,
  median price $32.
- Spain — Pedro Ximénez: 32 records, mean rating 90.16,
  median price $21.50.
- Italy — Nebbiolo: 934 records, mean rating 90.33,
  median price $57.

These examples illustrate how price and rating patterns differ
across combinations. They should not be interpreted as a universal
ranking of wine quality or value.

## 9. Correlations by Country and Variety

The group-level correlation analysis required at least 50 records
per country-variety combination.

The analysis identified 178 qualifying combinations.

Examples of strong positive Spearman correlations included:

- Italy — Merlot: 0.8331.
- Spain — Tinto Fino: 0.8191.
- France — Chardonnay: 0.7945.
- Italy — Syrah: 0.7871.
- Italy — Montepulciano: 0.7857.

Some combinations had weak or slightly negative associations.
For example, Spain — Rosé had a Spearman correlation of -0.0964.

This indicates that the price-rating relationship varies by
country-variety segment. Correlations from smaller groups may be
less stable than those supported by larger samples.

## 10. Price Sensitivity Analysis

A sensitivity analysis compared group-level correlations before
and after excluding records priced above the overall 99th percentile.

The threshold was approximately $152.73.

- Full eligible dataset: 89,128 records.
- Price-filtered dataset: 88,236 records.
- Records excluded from the sensitivity analysis: 892.
- Comparable country-variety groups: 175.

Across these comparable groups:

- Mean Pearson correlation changed from 0.4479 to 0.4644.
- Mean Spearman correlation changed from 0.4948 to 0.4891.
- Median absolute Spearman change rounded to 0.0000 at four decimals.

Several individual groups showed larger changes, especially in
Pearson correlation. This demonstrates that the influence of
extreme prices can differ across wine segments.

The filtered records were excluded only from this sensitivity
comparison. The primary dataset remains unchanged, and expensive
records are not automatically treated as errors.

## 11. Business Insights

The analyses support the following descriptive insights:

1. Listed prices are strongly right-skewed, so medians and
   percentiles are useful alongside averages.
2. Higher price bands generally have higher mean critic ratings
   in this dataset.
3. Affordable, highly rated records exist across multiple countries
   and varieties.
4. Price-rating associations vary across country-variety segments.
5. Extreme prices influence some group-level correlations more
   than others.
6. Comparisons should include sample sizes and clear eligibility
   rules to avoid overinterpreting small groups.

## 12. Limitations

- The dataset contains critic review records, not verified sales
  or transaction data.
- Duplicate-looking records cannot always be confirmed as errors
  because a reliable unique review identifier is unavailable.
- Missing prices and geographic fields limit some analyses.
- Correlation does not establish causation.
- The analysis does not establish consumer preferences, demand,
  profitability or market share.
- Findings may depend on price thresholds, rating thresholds,
  sample-size rules and the composition of the dataset.
- Historical listed prices should not automatically be interpreted
  as current retail prices.

## 13. Outputs and Visualisations

Key generated outputs include:

- `reports/figures/01_price_distribution.png`
- `reports/figures/02_rating_distribution.png`
- `reports/figures/03_price_vs_rating.png`
- `reports/figures/04_strongest_country_variety_correlations.png`
- `reports/figures/05_weakest_country_variety_correlations.png`
- `reports/country_variety_value_analysis.csv`
- `reports/overall_country_variety_analysis.csv`
- `reports/country_variety_correlation.csv`
- `reports/price_outlier_sensitivity.csv`

Additional cleaning and analysis decisions are documented in
`reports/data_cleaning_decisions.md`.

## 14. Recommended Next Phase

The next phase is SQL-based analysis.

The planned work is to load the analytical dataset into MySQL,
validate the imported data, and reproduce selected findings using
SQL queries, aggregations, joins and subqueries.

After SQL validation, the project can progress to Excel-based
analysis and Power BI dashboard development.

---

**End of report**
"""

# --------------------------------------------------
# 4. Add a small consistency check before saving
# --------------------------------------------------

print("EDA SUMMARY REPORT")
print("=" * 60)

print(f"Correlation report rows: {len(correlations):,}")
print(f"Sensitivity report rows: {len(sensitivity):,}")
print(f"Value-analysis rows: {len(value_analysis):,}")
print(f"Overall country-variety rows: {len(overall_analysis):,}")

# --------------------------------------------------
# 5. Save the report
# --------------------------------------------------

OUTPUT_FILE.write_text(report, encoding="utf-8")

print(f"\nReport saved successfully:\n{OUTPUT_FILE}")
print(f"Report size: {OUTPUT_FILE.stat().st_size:,} bytes")
