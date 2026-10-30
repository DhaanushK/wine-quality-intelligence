# Data Cleaning Decisions

## Decision 1: Preserve the original dataset

The original `winemag-data_first150k.csv` file will remain unchanged throughout the project.

## Decision 2: Create a separate analytical dataset

A separate working copy will be created for data cleaning and analysis. The original source data will never be overwritten.

## Decision 3: Investigate exact duplicates

The column `Unnamed: 0` appears to be a sequential index. Duplicate checks will exclude this column because it does not represent a meaningful wine attribute.

The initial audit identified:
- Original records: 150,930
- Distinct record combinations after excluding the index: 97,851
- Rows belonging to repeated-record groups: 92,366
- Repeated occurrences beyond the first: 53,079

## Decision 4: Compare before and after deduplication

We will compare record counts, price statistics, critic-rating distributions and selected country and variety summaries before and after deduplication.

## Decision 5: Avoid unsupported assumptions

Identical records will not automatically be described as erroneous source entries. Since the dataset does not provide a reliable unique review identifier, we cannot establish whether every repeated record represents an accidental duplication.

## Decision 6: Document the final decision

The deduplicated version will be considered for the main descriptive analysis, subject to validation of the comparison results. Any limitations caused by deduplication will be documented in the final report.

## Decision 7: Investigate missing and unusually high prices

The price audit identified:
- Total records: 150,930
- Records with available prices: 137,235
- Missing prices: 13,695 (9.07%)
- Median price: 24
- Mean price: 33.13
- 99th-percentile price: 150
- Maximum price: 2,300

The interquartile range (IQR) method flagged 7,582 prices (5.52% of records with available prices) as potential statistical outliers.

**Decision:** Retain the original prices for now. Statistical outliers will not automatically be deleted, capped, or replaced because expensive wines may have legitimate high prices. Records with missing prices will be excluded only from analyses that require price, unless a specific, justified treatment is established later.

The dataset's listed prices will be treated as recorded values. Currency conversion and inflation adjustments are outside the current cleaning scope unless additional reliable metadata becomes available.

The original dataset remains unchanged.

## Decision 8: Handle missing geographical information

The categorical quality audit identified 5 records with missing country and province information. These records also lack region_1 and region_2 values, but retain variety and winery information.

**Decision:** Retain these records in the working dataset. Do not infer missing geographical values without reliable supporting evidence. Exclude records only from analyses that require the missing geographical information.

## Decision 9: Standardize text only when justified

The audit found no leading or trailing spaces in country, province, or region_2 values. It identified potential whitespace issues in:
- region_1: 3 values
- variety: 12 values
- winery: 3 values

No country labels differing only by capitalization were detected.

**Decision:** Inspect the affected values before standardizing them. If the spaces are unnecessary formatting differences, remove leading and trailing whitespace in the analytical copy while preserving the original dataset. Record the changes made during cleaning.

## Decision 10: Remove unnecessary outer whitespace

The inspection confirmed the following affected rows:
- region_1: 3 rows containing "Bordeaux Côtes de Francs"
- variety: 2 rows containing "Tintilia" and 10 rows containing "Verduzzo Friulano"
- winery: 3 rows containing "A.R. Lenoble"

The differences are leading or trailing spaces around otherwise identical labels.

**Decision:** Remove leading and trailing whitespace from text fields in the analytical dataset. Preserve the original CSV unchanged. Missing values will remain missing until a specific analysis requires a justified treatment.

## Decision 11: Preserve both versions for duplicate sensitivity analysis

The comparison found:
- Cleaned records before deduplication: 150,930
- Records after exact deduplication: 97,851
- Rows removed: 53,079 (35.17%)

The mean price changed from 33.13 to 33.66, while the median price changed from 24 to 25. The mean rating changed from 87.89 to 87.96, and the median rating remained 88.

Country and variety record counts also decreased substantially after deduplication.

**Decision:** Preserve the cleaned dataset with all rows and create a separate deduplicated dataset. Use the deduplicated version as an initial candidate for analysis of distinct recorded combinations, and compare important findings against the full cleaned dataset. Do not assume every repeated record is erroneous, because a reliable unique review identifier is unavailable.

Document the chosen dataset and the effect of deduplication when presenting analytical results.

## Decision 12: Validate findings against duplicate handling

The sensitivity analysis compared the all-cleaned-records dataset with the deduplicated dataset using the same price and rating thresholds.

Results:
- Eligible records with all cleaned rows: 13,164
- Eligible records after deduplication: 8,912
- Country-variety combinations meeting the minimum group size in both datasets: 84
- US Riesling mean rating: 91.20 before deduplication and 91.16 after deduplication
- Portuguese Red mean rating: 90.97 before deduplication and 90.99 after deduplication

The mean prices and ratings for these two combinations remained similar across the two versions, although their record counts decreased substantially after deduplication.

**Decision:** Retain both datasets and use the deduplicated dataset as the primary candidate for descriptive analysis of distinct recorded combinations. Preserve the all-cleaned-records dataset for sensitivity comparisons. Do not interpret either dataset's record counts as unique verified reviews, sales volume, or market share.