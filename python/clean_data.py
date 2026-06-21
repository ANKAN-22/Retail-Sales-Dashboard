"""
Retail Sales Data Cleaning Script
------------------------------------
Loads raw retail sales data and performs cleaning:
- Removes duplicates
- Handles missing values
- Standardizes date formats
- Fixes inconsistent category names
- Verifies/corrects data types
- Creates calculated columns (Profit Margin, Revenue per Customer, Average Order Value)

Input:  ../dataset/retail_sales_raw.csv
Output: ../dataset/retail_sales_clean.csv
"""

import pandas as pd
import numpy as np

# ---- 1. Load data ----
df = pd.read_csv("../dataset/retail_sales_raw.csv")
print(f"Raw rows: {len(df)}")

# ---- 2. Remove duplicates ----
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

# ---- 3. Standardize Product_Category (fix casing/typos) ----
category_map = {
    "electronics": "Electronics", "ELECTRONICS": "Electronics", "Electronic": "Electronics",
    "Electronics ": "Electronics", "electronics ": "Electronics",
    "furniture": "Furniture", "FURNITURE": "Furniture", "Furnitures": "Furniture",
    "clothing": "Clothing", "Clothes": "Clothing", "CLOTHING": "Clothing",
    "groceries": "Groceries", "Grocery": "Groceries", "GROCERIES": "Groceries",
    "home decor": "Home Decor", "HomeDecor": "Home Decor", "Home decor": "Home Decor",
    "sports": "Sports", "SPORTS": "Sports", "Sport": "Sports",
    "stationery": "Stationery", "STATIONERY": "Stationery", "Stationary": "Stationery",
}
df["Product_Category"] = df["Product_Category"].astype(str).str.strip()
df["Product_Category"] = df["Product_Category"].replace(category_map)
df.loc[df["Product_Category"] == "nan", "Product_Category"] = np.nan

# Fill missing category using Product_Name (most common category for that product)
product_to_category = df.dropna(subset=["Product_Category"]).groupby("Product_Name")["Product_Category"].agg(
    lambda x: x.mode()[0] if not x.mode().empty else np.nan
)
df["Product_Category"] = df.apply(
    lambda row: product_to_category.get(row["Product_Name"], row["Product_Category"])
    if pd.isna(row["Product_Category"]) else row["Product_Category"],
    axis=1
)

# ---- 4. Standardize Order_Date (multiple formats -> YYYY-MM-DD) ----
def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d-%b-%Y"):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["Order_Date"] = df["Order_Date"].apply(parse_date)
print(f"Unparseable dates: {df['Order_Date'].isna().sum()}")

# ---- 5. Handle missing values ----
# Customer_Name: fill from Customer_ID using other rows with same ID
name_lookup = df.dropna(subset=["Customer_Name"]).drop_duplicates("Customer_ID").set_index("Customer_ID")["Customer_Name"]
df["Customer_Name"] = df.apply(
    lambda row: name_lookup.get(row["Customer_ID"], "Unknown") if pd.isna(row["Customer_Name"]) else row["Customer_Name"],
    axis=1
)

# Region: fill from Customer_ID using other rows with same ID
region_lookup = df.dropna(subset=["Region"]).drop_duplicates("Customer_ID").set_index("Customer_ID")["Region"]
df["Region"] = df.apply(
    lambda row: region_lookup.get(row["Customer_ID"], "Unknown") if pd.isna(row["Region"]) else row["Region"],
    axis=1
)

# Unit_Price: fill missing using Revenue / Quantity where possible, else median price for that product
df["Unit_Price"] = df.apply(
    lambda row: round(row["Revenue"] / row["Quantity"], 2)
    if pd.isna(row["Unit_Price"]) and row["Quantity"] not in (0, np.nan)
    else row["Unit_Price"],
    axis=1
)
df["Unit_Price"] = df["Unit_Price"].fillna(df.groupby("Product_Name")["Unit_Price"].transform("median"))

# Drop rows still missing critical fields after fill attempts
critical_cols = ["Order_ID", "Customer_ID", "Quantity", "Revenue", "Profit", "Order_Date"]
before = len(df)
df = df.dropna(subset=critical_cols)
print(f"Dropped {before - len(df)} rows with missing critical fields")

# ---- 6. Verify / correct data types ----
df["Quantity"] = df["Quantity"].astype(int)
df["Unit_Price"] = df["Unit_Price"].astype(float)
df["Revenue"] = df["Revenue"].astype(float)
df["Profit"] = df["Profit"].astype(float)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# ---- 7. Calculated columns ----
df["Profit_Margin_Pct"] = round((df["Profit"] / df["Revenue"]) * 100, 2)

revenue_per_customer = df.groupby("Customer_ID")["Revenue"].sum().rename("Revenue_Per_Customer")
df = df.merge(revenue_per_customer, on="Customer_ID", how="left")

avg_order_value = df["Revenue"].mean()
df["Avg_Order_Value"] = round(avg_order_value, 2)  # overall AOV reference column

# Extra useful time columns for dashboard
df["Order_Year"] = df["Order_Date"].dt.year
df["Order_Month"] = df["Order_Date"].dt.month
df["Order_Quarter"] = df["Order_Date"].dt.quarter

# ---- 8. Final checks ----
print("\nFinal dataset info:")
print(df.info())
print(f"\nFinal row count: {len(df)}")
print(f"Missing values per column:\n{df.isna().sum()}")

# ---- 9. Save ----
output_path = "../dataset/retail_sales_clean.csv"
df.to_csv(output_path, index=False)
print(f"\nClean dataset saved -> {output_path}")