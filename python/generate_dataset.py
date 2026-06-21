"""
Retail Sales Dataset Generator
--------------------------------
Generates a synthetic retail sales dataset with realistic "messiness"
(duplicates, missing values, inconsistent category names) so that
real data cleaning work can be demonstrated in Step 2.

Output: ../dataset/retail_sales_raw.csv
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

NUM_RECORDS = 8000

# ---- Reference data ----
categories_clean = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Tablet", "Smartwatch", "Bluetooth Speaker", "Camera"],
    "Furniture": ["Office Chair", "Dining Table", "Bookshelf", "Sofa", "Bed Frame", "Coffee Table"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Hoodie"],
    "Groceries": ["Coffee Beans", "Olive Oil", "Rice Bag", "Cereal", "Snack Box", "Tea Pack"],
    "Home Decor": ["Wall Clock", "Table Lamp", "Photo Frame", "Curtains", "Rug", "Wall Art"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Football", "Tennis Racket", "Running Shoes", "Bicycle"],
    "Stationery": ["Notebook", "Pen Set", "Backpack", "Desk Organizer", "Sketchbook"],
}

# Inconsistent category name variants (to simulate messy real-world data)
category_variants = {
    "Electronics": ["Electronics", "electronics", "ELECTRONICS", "Electronic", "Electronics "],
    "Furniture": ["Furniture", "furniture", "FURNITURE", "Furnitures"],
    "Clothing": ["Clothing", "clothing", "Clothes", "CLOTHING"],
    "Groceries": ["Groceries", "groceries", "Grocery", "GROCERIES"],
    "Home Decor": ["Home Decor", "home decor", "HomeDecor", "Home decor"],
    "Sports": ["Sports", "sports", "SPORTS", "Sport"],
    "Stationery": ["Stationery", "stationery", "STATIONERY", "Stationary"],
}

regions = {
    "North": ["Delhi", "Chandigarh", "Lucknow", "Jaipur"],
    "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi"],
    "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati"],
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat"],
}

# ---- Generate customers (so some customers repeat orders -> retention analysis) ----
NUM_CUSTOMERS = 1800
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "Customer_ID": f"CUST{i:05d}",
        "Customer_Name": fake.name(),
        "Region": random.choice(list(regions.keys())),
    })

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for order_num in range(1, NUM_RECORDS + 1):
    customer = random.choice(customers)
    region = customer["Region"]
    state_city = random.choice(regions[region])

    category_clean = random.choice(list(categories_clean.keys()))
    product = random.choice(categories_clean[category_clean])
    category_display = random.choice(category_variants[category_clean])  # messy variant

    quantity = random.randint(1, 8)
    unit_price = round(random.uniform(150, 25000), 2)
    revenue = round(quantity * unit_price, 2)
    profit_margin_pct = random.uniform(0.05, 0.35)
    profit = round(revenue * profit_margin_pct, 2)

    order_date = start_date + timedelta(days=random.randint(0, date_range_days))

    # Randomly choose a date format to simulate inconsistency
    date_format = random.choice(["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d-%b-%Y"])
    order_date_str = order_date.strftime(date_format)

    row = {
        "Order_ID": f"ORD{order_num:06d}",
        "Customer_ID": customer["Customer_ID"],
        "Customer_Name": customer["Customer_Name"],
        "Product_Name": product,
        "Product_Category": category_display,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Revenue": revenue,
        "Profit": profit,
        "Order_Date": order_date_str,
        "Region": region,
        "State_City": state_city,
    }
    rows.append(row)

df = pd.DataFrame(rows)

# ---- Inject messiness ----

# 1. Duplicates (~2% of rows duplicated)
dup_count = int(NUM_RECORDS * 0.02)
dup_rows = df.sample(n=dup_count, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

# 2. Missing values in a few columns
for col, frac in [("Customer_Name", 0.01), ("Unit_Price", 0.015), ("Region", 0.01), ("Product_Category", 0.005)]:
    idx = df.sample(frac=frac, random_state=2).index
    df.loc[idx, col] = np.nan

# 3. Shuffle row order
df = df.sample(frac=1, random_state=3).reset_index(drop=True)

# ---- Save ----
output_path = "../dataset/retail_sales_raw.csv"
df.to_csv(output_path, index=False)

print(f"Dataset generated: {len(df)} rows -> {output_path}")
print(df.head())