"""
Generates a realistic, messy raw retail sales dataset for the
Data Cleaning & Visualization project.

Intentional data quality issues injected:
- Missing values (various columns)
- Duplicate rows
- Outliers in Sales/Quantity/Price
- Inconsistent text casing / whitespace in categorical fields
- Mixed date formats
- Negative values where impossible (data entry errors)
"""

import numpy as np
import pandas as pd

np.random.seed(42)

n = 2000

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books"]
payment_methods = ["Credit Card", "Debit Card", "Cash", "UPI", "Wallet"]

start_date = pd.Timestamp("2023-01-01")
dates = start_date + pd.to_timedelta(np.random.randint(0, 730, size=n), unit="D")

df = pd.DataFrame({
    "OrderID": np.arange(1001, 1001 + n),
    "OrderDate": dates,
    "CustomerID": np.random.randint(1, 500, size=n),
    "Region": np.random.choice(regions, size=n),
    "Category": np.random.choice(categories, size=n),
    "Quantity": np.random.randint(1, 10, size=n),
    "UnitPrice": np.round(np.random.uniform(5, 500, size=n), 2),
    "PaymentMethod": np.random.choice(payment_methods, size=n),
    "CustomerAge": np.random.randint(18, 70, size=n),
})

df["Sales"] = np.round(df["Quantity"] * df["UnitPrice"], 2)

# --- Inject messiness ---

# 1. Missing values
for col, frac in [("UnitPrice", 0.04), ("CustomerAge", 0.06),
                   ("Region", 0.02), ("PaymentMethod", 0.03), ("Sales", 0.03)]:
    idx = np.random.choice(df.index, size=int(len(df) * frac), replace=False)
    df.loc[idx, col] = np.nan

# 2. Duplicate rows (~2%)
dupes = df.sample(frac=0.02, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

# 3. Outliers
outlier_idx = np.random.choice(df.index, size=15, replace=False)
df.loc[outlier_idx, "Sales"] = df.loc[outlier_idx, "Sales"] * np.random.uniform(15, 40)
outlier_idx2 = np.random.choice(df.index, size=10, replace=False)
df.loc[outlier_idx2, "Quantity"] = np.random.randint(200, 500, size=10)

# 4. Impossible negative values (entry errors)
neg_idx = np.random.choice(df.index, size=8, replace=False)
df.loc[neg_idx, "UnitPrice"] = -df.loc[neg_idx, "UnitPrice"]

# 5. Inconsistent categorical text (casing/whitespace)
df["Category"] = df["Category"].astype(object)
messy_idx = np.random.choice(df.index, size=int(len(df) * 0.08), replace=False)
def messify(x):
    choice = np.random.choice(["lower", "upper", "space"])
    if choice == "lower":
        return str(x).lower()
    elif choice == "upper":
        return str(x).upper()
    else:
        return f"  {x}  "
df.loc[messy_idx, "Category"] = df.loc[messy_idx, "Category"].apply(messify)

# 6. Mixed date formats (store some as strings in different formats)
df["OrderDate"] = df["OrderDate"].astype(object)
alt_fmt_idx = np.random.choice(df.index, size=int(len(df) * 0.1), replace=False)
def alt_format(d):
    d = pd.Timestamp(d)
    fmt = np.random.choice(["%d/%m/%Y", "%m-%d-%Y", "%Y.%m.%d"])
    return d.strftime(fmt)
df.loc[alt_fmt_idx, "OrderDate"] = df.loc[alt_fmt_idx, "OrderDate"].apply(alt_format)

# Shuffle rows
df = df.sample(frac=1, random_state=7).reset_index(drop=True)

df.to_csv("/home/claude/project/data/raw_sales_data.csv", index=False)
print("Raw dataset created:", df.shape)
print(df.head())
