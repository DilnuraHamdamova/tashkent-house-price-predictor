# Dataset card

## Source and license

- Dataset: [Real estate prices in Tashkent, Uzbekistan](https://www.kaggle.com/datasets/anvarnarz/tashkent-real-estate-2019)
- Original publisher: Kaggle user Anvar Narzullaev
- Collection: scraped from the uybor.uz advertisement site in 2019
- License shown on the dataset card: **CC0: Public Domain**
- Repository file: `house_prices.csv` (converted from the source `uybor.xlsx` without changing values)

The file is included so the assessed workflow is reproducible without Kaggle credentials. It contains public property advertisements and no seller names, phone numbers, or credentials.

## Schema

| Column | Meaning | Use |
|---|---|---|
| `address` | Approximate listing address | Audit only; excluded from modeling |
| `district` | Tashkent district | Categorical feature |
| `rooms` | Number of rooms | Numeric feature |
| `size` | Apartment size in square metres | Numeric feature |
| `level` | Apartment floor | Numeric feature |
| `max_levels` | Floors in the building | Numeric feature |
| `price` | Advertised price in USD | Regression target |
| `lat` | Latitude | Numeric feature |
| `lng` | Longitude | Numeric feature |

`floor_ratio = level / max_levels` is calculated at runtime. Target-derived features such as price per square metre are deliberately excluded.

## Quality and preprocessing decisions

- Source rows: 7,421
- Exact duplicate rows: 696; removed inside `load_dataset` before splitting
- Rows used for modeling: 6,725
- Missing required values: 0
- Districts: 12
- Invalid `level > max_levels`: 0
- Outliers are retained because automatic IQR deletion would also remove legitimate luxury properties. Their impact is documented in error analysis.

## Limitations

The sample contains advertisements rather than completed transactions and is frozen in 2019. District representation is uneven (Bektemir and Yangihayot are especially sparse). The data lacks condition, construction year, renovation, legal status, and listing date. It should be used for education and historical analysis, not current professional appraisal.
