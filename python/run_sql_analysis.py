"""
Run SQL Analysis Queries
---------------------------
Executes each business analysis query from analysis_queries.sql against
the SQLite database and prints the results. Useful for verifying queries
and for pulling quick results into screenshots/documentation.

Input: ../sql/retail_sales.db
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("../sql/retail_sales.db")

queries = {
    "1. Total Revenue & Profit": """
        SELECT
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            ROUND(SUM(Profit) * 100.0 / SUM(Revenue), 2) AS Overall_Profit_Margin_Pct
        FROM sales;
    """,

    "2. Total Orders & Customers": """
        SELECT
            COUNT(DISTINCT Order_ID) AS Total_Orders,
            COUNT(DISTINCT Customer_ID) AS Total_Customers,
            ROUND(SUM(Revenue) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
        FROM sales;
    """,

    "3. Monthly Sales Trend (first 6 rows)": """
        SELECT Order_Year, Order_Month,
            ROUND(SUM(Revenue), 2) AS Monthly_Revenue,
            ROUND(SUM(Profit), 2) AS Monthly_Profit,
            COUNT(DISTINCT Order_ID) AS Orders
        FROM sales
        GROUP BY Order_Year, Order_Month
        ORDER BY Order_Year, Order_Month
        LIMIT 6;
    """,

    "5. Top 10 Products by Revenue": """
        SELECT Product_Name, Product_Category,
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            SUM(Quantity) AS Units_Sold
        FROM sales
        GROUP BY Product_Name, Product_Category
        ORDER BY Total_Revenue DESC
        LIMIT 10;
    """,

    "7. Category Performance": """
        SELECT Product_Category,
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            ROUND(SUM(Profit) * 100.0 / SUM(Revenue), 2) AS Profit_Margin_Pct,
            SUM(Quantity) AS Units_Sold,
            COUNT(DISTINCT Order_ID) AS Orders
        FROM sales
        GROUP BY Product_Category
        ORDER BY Total_Revenue DESC;
    """,

    "8. Best Region by Revenue": """
        SELECT Region,
            ROUND(SUM(Revenue), 2) AS Total_Revenue,
            ROUND(SUM(Profit), 2) AS Total_Profit,
            COUNT(DISTINCT Order_ID) AS Orders,
            COUNT(DISTINCT Customer_ID) AS Customers
        FROM sales
        GROUP BY Region
        ORDER BY Total_Revenue DESC;
    """,

    "11. Top 10 Customers by Revenue": """
        SELECT Customer_ID, Customer_Name,
            ROUND(SUM(Revenue), 2) AS Total_Spent,
            COUNT(DISTINCT Order_ID) AS Total_Orders,
            ROUND(SUM(Revenue) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
        FROM sales
        GROUP BY Customer_ID, Customer_Name
        ORDER BY Total_Spent DESC
        LIMIT 10;
    """,

    "12. Customer Purchase Frequency": """
        SELECT Order_Count_Bucket, COUNT(*) AS Number_Of_Customers
        FROM (
            SELECT Customer_ID, COUNT(DISTINCT Order_ID) AS Order_Count,
                CASE
                    WHEN COUNT(DISTINCT Order_ID) = 1 THEN '1 order (New)'
                    WHEN COUNT(DISTINCT Order_ID) BETWEEN 2 AND 3 THEN '2-3 orders'
                    WHEN COUNT(DISTINCT Order_ID) BETWEEN 4 AND 6 THEN '4-6 orders'
                    ELSE '7+ orders (Loyal)'
                END AS Order_Count_Bucket
            FROM sales
            GROUP BY Customer_ID
        ) AS customer_orders
        GROUP BY Order_Count_Bucket
        ORDER BY Number_Of_Customers DESC;
    """,
}

for title, query in queries.items():
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()