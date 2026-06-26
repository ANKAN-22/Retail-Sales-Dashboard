"""
Exploratory Data Analysis & Visualization
---------------------------------------------
Generates exploratory charts from the clean retail sales data using
Matplotlib. Charts are saved as PNG images for use in documentation
and to sanity-check trends before building the Power BI dashboard.

Input:  ../dataset/retail_sales_clean.csv
Output: ../screenshots/eda_*.png
"""

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3

df = pd.read_csv("../dataset/retail_sales_clean.csv", parse_dates=["Order_Date"])

# ---- 1. Monthly Revenue Trend ----
monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"].sum()
plt.figure()
monthly.plot(kind="line", marker="o", color="#2563eb")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("../screenshots/eda_monthly_revenue_trend.png", dpi=150)
plt.close()

# ---- 2. Top 10 Products by Revenue ----
top_products = df.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False).head(10)
plt.figure()
top_products.sort_values().plot(kind="barh", color="#16a34a")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (₹)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("../screenshots/eda_top10_products.png", dpi=150)
plt.close()

# ---- 3. Revenue by Category ----
category_rev = df.groupby("Product_Category")["Revenue"].sum().sort_values(ascending=False)
plt.figure()
category_rev.plot(kind="bar", color="#d97706")
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("../screenshots/eda_revenue_by_category.png", dpi=150)
plt.close()

# ---- 4. Revenue & Profit by Region ----
region_summary = df.groupby("Region")[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False)
plt.figure()
region_summary.plot(kind="bar", color=["#2563eb", "#16a34a"])
plt.title("Revenue & Profit by Region")
plt.xlabel("Region")
plt.ylabel("Amount (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("../screenshots/eda_revenue_profit_by_region.png", dpi=150)
plt.close()

# ---- 5. Profit Margin Distribution ----
plt.figure()
df["Profit_Margin_Pct"].plot(kind="hist", bins=30, color="#7c3aed", edgecolor="white")
plt.title("Distribution of Profit Margin %")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig("../screenshots/eda_profit_margin_distribution.png", dpi=150)
plt.close()

# ---- 6. Customer Order Frequency ----
order_freq = df.groupby("Customer_ID")["Order_ID"].nunique()
bins = [0, 1, 3, 6, 100]
labels = ["1 order", "2-3 orders", "4-6 orders", "7+ orders"]
freq_buckets = pd.cut(order_freq, bins=bins, labels=labels).value_counts().reindex(labels)
plt.figure()
freq_buckets.plot(kind="bar", color="#dc2626")
plt.title("Customer Purchase Frequency")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("../screenshots/eda_customer_frequency.png", dpi=150)
plt.close()

print("EDA complete. 6 charts saved to ../screenshots/")
print(" - eda_monthly_revenue_trend.png")
print(" - eda_top10_products.png")
print(" - eda_revenue_by_category.png")
print(" - eda_revenue_profit_by_region.png")
print(" - eda_profit_margin_distribution.png")
print(" - eda_customer_frequency.png")