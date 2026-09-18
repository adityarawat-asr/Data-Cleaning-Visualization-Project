# Data Cleaning & Visualization Project — Retail Sales

A complete, runnable mini-project: a messy raw dataset, a cleaning
pipeline, and a set of visualizations / dashboard telling the story
of the data.

## Folder structure

```
project/
├── data/
│   ├── generate_raw_data.py     # creates the messy raw dataset (already run)
│   ├── raw_sales_data.csv       # RAW data (2,040 rows, with issues)
│   └── cleaned_sales_data.csv   # CLEANED data (2,002 rows, output of step 1)
├── notebooks/
│   ├── 01_data_cleaning.py      # cleaning / preprocessing pipeline
│   └── 02_visualization.py      # chart + dashboard generation
├── outputs/
│   ├── 01_monthly_sales_trend.png
│   ├── 02_sales_by_category.png
│   ├── 03_sales_by_region.png
│   ├── 04_payment_method_distribution.png
│   ├── 05_customer_age_distribution.png
│   ├── 06_sales_boxplot_by_category.png
│   ├── 07_sales_by_weekday.png
│   ├── 08_correlation_heatmap.png
│   └── dashboard.png            # combined 6-panel dashboard
└── report/
    └── cleaning_log.txt         # exact log of every fix applied
```

## How to run it yourself

```bash
pip install pandas numpy matplotlib seaborn

python data/generate_raw_data.py     # (optional — raw CSV already included)
python notebooks/01_data_cleaning.py # cleans raw -> cleaned_sales_data.csv
python notebooks/02_visualization.py # builds charts + dashboard.png
```

## Data quality issues handled

| Issue | How it was fixed |
|---|---|
| Missing values (Region, UnitPrice, PaymentMethod, CustomerAge, Sales) | Median imputation (grouped by Category for price), mode imputation for categoricals, recomputed `Sales` from `Quantity × UnitPrice` where blank |
| Duplicate rows (~2%) | Detected and dropped with `drop_duplicates` (ignoring the OrderID key) |
| Outliers in `Sales` and `Quantity` | Detected via IQR method (1.5×IQR) and capped (winsorized) rather than deleted, to preserve sample size |
| Impossible negative prices | Corrected via absolute value |
| Inconsistent text casing/whitespace (`" electronics "`, `"CLOTHING"`, etc.) | Stripped and standardized to title case |
| Mixed date formats (`DD/MM/YYYY`, `MM-DD-YYYY`, `YYYY.MM.DD`) | Parsed with pandas flexible/mixed date parsing into a single `datetime64` column |

Full run-by-run log with row counts is in `report/cleaning_log.txt`.

## Key findings (from the cleaned data)

- **Total sales:** ~$2.44M across 2,002 valid orders (avg order value ≈ $1,218)
- **Top category by revenue:** Clothing, followed closely by Books and Sports
- **Regional split is fairly even** (23–28% each), with **North** slightly leading
- **UPI and Debit Card** are the most-used payment methods; **Cash** is least common
- **Customer age** is broadly spread 18–70 with a mild concentration in the 40s
- Sales show **no strong single-day-of-week effect** — Thursday and Saturday are marginally higher
- `Sales` correlates strongly with `Quantity` and `UnitPrice` (as expected structurally), with weak-to-no correlation against `CustomerAge`

## Notes / extension ideas

- Swap `generate_raw_data.py`'s output for your own raw CSV — just match the
  column names or edit `01_data_cleaning.py` accordingly.
- The pipeline is modular: cleaning and visualization are separate scripts
  so you can re-run just the charts after tweaking cleaning logic.
- Easy extensions: cohort/retention analysis by `CustomerID`, RFM segmentation,
  or an interactive dashboard (Plotly Dash / Streamlit) on top of `cleaned_sales_data.csv`.
