"""
Load Clean Data into SQLite Database
--------------------------------------
Reads the cleaned retail sales CSV and loads it into a SQLite database
so SQL analysis can be performed on it.

Input:  ../dataset/retail_sales_clean.csv
Output: ../sql/retail_sales.db
"""

import pandas as pd
import sqlite3

# ---- Load clean CSV ----
df = pd.read_csv("../dataset/retail_sales_clean.csv", parse_dates=["Order_Date"])
print(f"Loaded {len(df)} rows from CSV")

# ---- Connect to SQLite (creates file if it doesn't exist) ----
conn = sqlite3.connect("../sql/retail_sales.db")

# ---- Write to a table called 'sales' (replace if it already exists) ----
df.to_sql("sales", conn, if_exists="replace", index=False)
print("Data loaded into table 'sales'")

# ---- Verify ----
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")
row_count = cursor.fetchone()[0]
print(f"Row count in database: {row_count}")

cursor.execute("PRAGMA table_info(sales)")
print("\nColumns in 'sales' table:")
for col in cursor.fetchall():
    print(f"  {col[1]} ({col[2]})")

conn.close()
print("\nDatabase saved -> ../sql/retail_sales.db")