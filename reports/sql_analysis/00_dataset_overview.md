# Wine Quality Intelligence
## Dataset Overview and MySQL Validation

### Dataset Summary

The deduplicated dataset contains 97,851 wine review records covering 48 countries, 632 wine varieties and 14,795 wineries.

### Dataset Statistics

| Metric | Value |
|---|---:|
| Total review records | 97,851 |
| Unique countries | 48 |
| Unique varieties | 632 |
| Unique wineries | 14,795 |
| Records with listed prices | 89,131 |
| Records with missing prices | 8,720 |
| Average critic rating | 87.96 |
| Minimum critic rating | 80 |
| Maximum critic rating | 100 |
| Average listed price | $33.66 |
| Minimum listed price | $4.00 |
| Maximum listed price | $2,300.00 |

### Pricing Coverage

Approximately 91.09% of review records contain listed price information, while 8.91% have missing prices.

Pricing analysis therefore uses records with valid listed prices. Rating analysis can also include records without listed prices where appropriate.

### Validation

The MySQL dataset contains all 97,851 expected records. The missing-price count and overall rating and pricing aggregates agree with the Python analysis.

### Analytical Scope

This project examines critic ratings, listed prices, wine varieties, countries, wineries and regional patterns within the dataset. The findings represent the available review records and should not be interpreted as comprehensive measurements of global wine sales or market demand.