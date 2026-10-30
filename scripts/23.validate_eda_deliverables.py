from pathlib import Path
import pandas as pd

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"
REPORTS_DIR = PROJECT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# --------------------------------------------------
# 2. Define required files
# --------------------------------------------------

required_files = [
    DATA_DIR / "wine_reviews_cleaned.csv",
    DATA_DIR / "wine_reviews_deduplicated.csv",
    REPORTS_DIR / "data_cleaning_decisions.md",
    REPORTS_DIR / "eda_summary_report.md",
    REPORTS_DIR / "country_variety_value_analysis.csv",
    REPORTS_DIR / "overall_country_variety_analysis.csv",
    REPORTS_DIR / "country_variety_correlation.csv",
    REPORTS_DIR / "price_outlier_sensitivity.csv",
    FIGURES_DIR / "01_price_distribution.png",
    FIGURES_DIR / "02_rating_distribution.png",
    FIGURES_DIR / "03_price_vs_rating.png",
    FIGURES_DIR / "04_strongest_country_variety_correlations.png",
    FIGURES_DIR / "05_weakest_country_variety_correlations.png",
]

print("=" * 65)
print("EDA DELIVERABLE VALIDATION")
print("=" * 65)

passed = 0
failed = 0


def record_check(description, condition):
    global passed, failed

    if condition:
        print(f"[PASS] {description}")
        passed += 1
    else:
        print(f"[FAIL] {description}")
        failed += 1


# --------------------------------------------------
# 3. Check file existence
# --------------------------------------------------

print("\n1. FILE EXISTENCE CHECKS")

for file_path in required_files:
    record_check(
        f"{file_path.relative_to(PROJECT_DIR)} exists",
        file_path.is_file()
    )

# Stop before loading files if essential inputs are missing.
essential_files = [
    DATA_DIR / "wine_reviews_cleaned.csv",
    DATA_DIR / "wine_reviews_deduplicated.csv",
    REPORTS_DIR / "eda_summary_report.md",
    REPORTS_DIR / "country_variety_value_analysis.csv",
    REPORTS_DIR / "overall_country_variety_analysis.csv",
    REPORTS_DIR / "country_variety_correlation.csv",
    REPORTS_DIR / "price_outlier_sensitivity.csv",
]

missing_essential = [
    path for path in essential_files if not path.is_file()
]

if missing_essential:
    print("\nEssential files are missing. Fix these before continuing.")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    raise SystemExit(1)

# --------------------------------------------------
# 4. Validate datasets
# --------------------------------------------------

print("\n2. DATASET VALIDATION")

cleaned = pd.read_csv(DATA_DIR / "wine_reviews_cleaned.csv")
deduplicated = pd.read_csv(
    DATA_DIR / "wine_reviews_deduplicated.csv"
)

record_check(
    "Cleaned dataset contains 150,930 rows",
    len(cleaned) == 150930
)

record_check(
    "Deduplicated dataset contains 97,851 rows",
    len(deduplicated) == 97851
)

record_check(
    "Both analytical datasets have 10 columns",
    len(cleaned.columns) == 10
    and len(deduplicated.columns) == 10
)

record_check(
    "Deduplicated dataset has no exact duplicate rows",
    not deduplicated.duplicated().any()
)

record_check(
    "Both datasets exclude the original index column",
    "Unnamed: 0" not in cleaned.columns
    and "Unnamed: 0" not in deduplicated.columns
)

# --------------------------------------------------
# 5. Validate report CSV row counts
# --------------------------------------------------

print("\n3. ANALYSIS REPORT VALIDATION")

value_df = pd.read_csv(
    REPORTS_DIR / "country_variety_value_analysis.csv"
)

overall_df = pd.read_csv(
    REPORTS_DIR / "overall_country_variety_analysis.csv"
)

correlation_df = pd.read_csv(
    REPORTS_DIR / "country_variety_correlation.csv"
)

sensitivity_df = pd.read_csv(
    REPORTS_DIR / "price_outlier_sensitivity.csv"
)

record_check(
    "Affordable-value report contains 84 groups",
    len(value_df) == 84
)

record_check(
    "Overall country-variety report contains 242 groups",
    len(overall_df) == 242
)

record_check(
    "Correlation report contains 178 groups",
    len(correlation_df) == 178
)

record_check(
    "Sensitivity report contains 175 comparable groups",
    len(sensitivity_df) == 175
)

# --------------------------------------------------
# 6. Validate key statistics in the EDA report
# --------------------------------------------------

print("\n4. EDA REPORT CONTENT CHECKS")

report_path = REPORTS_DIR / "eda_summary_report.md"
report_text = report_path.read_text(encoding="utf-8")

required_report_text = [
    "150,930 records",
    "97,851 records",
    "Pearson correlation: 0.4474",
    "Spearman correlation: 0.5987",
    "8,912 matching records",
    "0.8331",
    "0.8191",
    "0.7945",
    "$152.73",
    "Limitations",
    "Recommended Next Phase",
]

for phrase in required_report_text:
    record_check(
        f"EDA report contains: {phrase}",
        phrase in report_text
    )

# --------------------------------------------------
# 7. Validate cleaning-decision documentation
# --------------------------------------------------

print("\n5. CLEANING DECISION DOCUMENTATION")

decisions_path = REPORTS_DIR / "data_cleaning_decisions.md"

if decisions_path.is_file():
    decisions_text = decisions_path.read_text(encoding="utf-8")

    record_check(
        "Cleaning decisions document is not empty",
        len(decisions_text.strip()) > 0
    )
else:
    record_check(
        "Cleaning decisions document exists",
        False
    )

# --------------------------------------------------
# 8. Final summary
# --------------------------------------------------

print("\n" + "=" * 65)
print("VALIDATION SUMMARY")
print("=" * 65)

print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")

if failed == 0:
    print("\nAll checks passed.")
    print("EDA deliverables are ready for final review.")
else:
    print("\nSome checks failed.")
    print("Review the [FAIL] messages before proceeding.")

print("=" * 65)

if failed > 0:
    raise SystemExit(1)
