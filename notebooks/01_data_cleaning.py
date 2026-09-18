"""
Data Cleaning & Preprocessing
==============================
Loads raw_sales_data.csv, cleans it, and writes cleaned_sales_data.csv
plus a cleaning log summarizing every fix applied.
"""

import pandas as pd
import numpy as np

RAW_PATH = "/home/claude/project/data/raw_sales_data.csv"
CLEAN_PATH = "/home/claude/project/data/cleaned_sales_data.csv"
LOG_PATH = "/home/claude/project/report/cleaning_log.txt"

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

df = pd.read_csv(RAW_PATH)
log(f"Raw shape: {df.shape}")

# ---------------------------------------------------------------
# 1. Standardize column types / parse mixed-format dates
# ---------------------------------------------------------------
df["OrderDate"] = pd.to_datetime(df["OrderDate"], format="mixed", dayfirst=False, errors="coerce")
log(f"Unparseable dates after coercion: {df['OrderDate'].isna().sum()}")

# ---------------------------------------------------------------
# 2. Clean categorical text (strip whitespace, title-case)
# ---------------------------------------------------------------
df["Category"] = df["Category"].astype(str).str.strip().str.title()
df["Region"] = df["Region"].astype(str).str.strip().str.title()
df.loc[df["Region"] == "Nan", "Region"] = np.nan

# ---------------------------------------------------------------
# 3. Remove duplicate rows
# ---------------------------------------------------------------
dup_count = df.duplicated(subset=[c for c in df.columns if c != "OrderID"]).sum()
df = df.drop_duplicates(subset=[c for c in df.columns if c != "OrderID"], keep="first")
log(f"Duplicate rows removed: {dup_count}")

# ---------------------------------------------------------------
# 4. Fix impossible values (negative prices -> absolute value)
# ---------------------------------------------------------------
neg_price_count = (df["UnitPrice"] < 0).sum()
df["UnitPrice"] = df["UnitPrice"].abs()
log(f"Negative UnitPrice values corrected (abs): {neg_price_count}")

# ---------------------------------------------------------------
# 5. Handle missing values
# ---------------------------------------------------------------
missing_before = df.isna().sum()
log("Missing values BEFORE imputation:\n" + str(missing_before[missing_before > 0]))

# Numeric: median imputation grouped by Category where possible
df["UnitPrice"] = df.groupby("Category")["UnitPrice"].transform(
    lambda x: x.fillna(x.median())
)
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median())

# Recompute Sales where missing or inconsistent with Quantity * UnitPrice
recalculated = df["Quantity"] * df["UnitPrice"]
sales_missing = df["Sales"].isna().sum()
df["Sales"] = df["Sales"].fillna(recalculated)

# Region / PaymentMethod: fill with mode (most frequent category)
df["Region"] = df["Region"].fillna(df["Region"].mode()[0])
df["PaymentMethod"] = df["PaymentMethod"].fillna(df["PaymentMethod"].mode()[0])

# Drop rows where OrderDate couldn't be parsed (critical field)
before_drop = len(df)
df = df.dropna(subset=["OrderDate"])
log(f"Rows dropped due to unparseable OrderDate: {before_drop - len(df)}")

missing_after = df.isna().sum()
log("Missing values AFTER imputation:\n" + str(missing_after[missing_after > 0]))

# ---------------------------------------------------------------
# 6. Outlier detection & treatment (IQR method) on Sales & Quantity
# ---------------------------------------------------------------
def iqr_bounds(series, k=1.5):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

for col in ["Sales", "Quantity"]:
    lo, hi = iqr_bounds(df[col])
    n_outliers = ((df[col] < lo) | (df[col] > hi)).sum()
    log(f"{col}: IQR bounds [{lo:.2f}, {hi:.2f}] -> {n_outliers} outliers capped")
    df[col] = df[col].clip(lower=max(lo, 0), upper=hi)

# Recompute Sales consistently after capping Quantity/UnitPrice
df["Sales"] = np.round(df["Quantity"] * df["UnitPrice"], 2)

# ---------------------------------------------------------------
# 7. Feature engineering (useful for visualization/storytelling)
# ---------------------------------------------------------------
df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
df["OrderYear"] = df["OrderDate"].dt.year
df["Weekday"] = df["OrderDate"].dt.day_name()

# ---------------------------------------------------------------
# 8. Final checks & save
# ---------------------------------------------------------------
log(f"Final cleaned shape: {df.shape}")
log(f"Remaining nulls total: {df.isna().sum().sum()}")

df.to_csv(CLEAN_PATH, index=False)
log(f"Cleaned data saved to {CLEAN_PATH}")

with open(LOG_PATH, "w") as f:
    f.write("\n\n".join(log_lines))

print("\nDone. Cleaning log written to", LOG_PATH)
