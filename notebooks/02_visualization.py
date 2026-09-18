"""
Visualization & Insights
=========================
Reads cleaned_sales_data.csv and produces:
- Individual PNG charts in /outputs
- A combined dashboard PNG (dashboard.png)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
OUT = "/home/claude/project/outputs"

df = pd.read_csv("/home/claude/project/data/cleaned_sales_data.csv", parse_dates=["OrderDate"])

# ---------------------------------------------------------------
# 1. Monthly sales trend
# ---------------------------------------------------------------
monthly = df.groupby("OrderMonth")["Sales"].sum().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly, x="OrderMonth", y="Sales", marker="o", color="#2b6cb0")
plt.xticks(rotation=75)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(f"{OUT}/01_monthly_sales_trend.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 2. Sales by category
# ---------------------------------------------------------------
cat_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(8, 5))
sns.barplot(data=cat_sales, x="Sales", y="Category", hue="Category", palette="viridis", legend=False)
plt.title("Total Sales by Category")
plt.xlabel("Total Sales")
plt.tight_layout()
plt.savefig(f"{OUT}/02_sales_by_category.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 3. Sales by region (pie)
# ---------------------------------------------------------------
region_sales = df.groupby("Region")["Sales"].sum()
plt.figure(figsize=(6, 6))
plt.pie(region_sales, labels=region_sales.index, autopct="%1.1f%%",
        colors=sns.color_palette("pastel"), startangle=90)
plt.title("Sales Share by Region")
plt.tight_layout()
plt.savefig(f"{OUT}/03_sales_by_region.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 4. Payment method distribution
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5))
order = df["PaymentMethod"].value_counts().index
sns.countplot(data=df, y="PaymentMethod", order=order, hue="PaymentMethod",
              palette="mako", legend=False)
plt.title("Order Count by Payment Method")
plt.xlabel("Number of Orders")
plt.tight_layout()
plt.savefig(f"{OUT}/04_payment_method_distribution.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 5. Customer age distribution
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.histplot(df["CustomerAge"], bins=20, kde=True, color="#805ad5")
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.tight_layout()
plt.savefig(f"{OUT}/05_customer_age_distribution.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 6. Sales distribution (boxplot) by category - post-cleaning outlier check
# ---------------------------------------------------------------
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x="Category", y="Sales", hue="Category", palette="Set2", legend=False)
plt.xticks(rotation=20)
plt.title("Sales Distribution by Category (post-cleaning)")
plt.tight_layout()
plt.savefig(f"{OUT}/06_sales_boxplot_by_category.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 7. Weekday sales pattern
# ---------------------------------------------------------------
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_sales = df.groupby("Weekday")["Sales"].sum().reindex(weekday_order).reset_index()
plt.figure(figsize=(9, 5))
sns.barplot(data=weekday_sales, x="Weekday", y="Sales", hue="Weekday", palette="crest", legend=False)
plt.title("Total Sales by Day of Week")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(f"{OUT}/07_sales_by_weekday.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# 8. Correlation heatmap
# ---------------------------------------------------------------
plt.figure(figsize=(6, 5))
corr = df[["Quantity", "UnitPrice", "Sales", "CustomerAge"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(f"{OUT}/08_correlation_heatmap.png", dpi=150)
plt.close()

# ---------------------------------------------------------------
# Combined dashboard (2x3 grid of key charts)
# ---------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(20, 11))
fig.suptitle("Retail Sales Dashboard", fontsize=20, fontweight="bold")

sns.lineplot(data=monthly, x="OrderMonth", y="Sales", marker="o", ax=axes[0, 0], color="#2b6cb0")
axes[0, 0].set_title("Monthly Sales Trend")
axes[0, 0].tick_params(axis="x", rotation=75)

sns.barplot(data=cat_sales, x="Sales", y="Category", hue="Category", palette="viridis",
            legend=False, ax=axes[0, 1])
axes[0, 1].set_title("Sales by Category")

axes[0, 2].pie(region_sales, labels=region_sales.index, autopct="%1.1f%%",
               colors=sns.color_palette("pastel"), startangle=90)
axes[0, 2].set_title("Sales Share by Region")

sns.countplot(data=df, y="PaymentMethod", order=order, hue="PaymentMethod",
              palette="mako", legend=False, ax=axes[1, 0])
axes[1, 0].set_title("Orders by Payment Method")

sns.histplot(df["CustomerAge"], bins=20, kde=True, color="#805ad5", ax=axes[1, 1])
axes[1, 1].set_title("Customer Age Distribution")

sns.barplot(data=weekday_sales, x="Weekday", y="Sales", hue="Weekday", palette="crest",
            legend=False, ax=axes[1, 2])
axes[1, 2].set_title("Sales by Weekday")
axes[1, 2].tick_params(axis="x", rotation=30)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(f"{OUT}/dashboard.png", dpi=150)
plt.close()

print("All charts + dashboard saved to", OUT)
