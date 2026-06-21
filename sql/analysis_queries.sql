-- ============================================================
-- Retail Sales & Customer Insights - SQL Analysis Queries
-- Database: retail_sales.db | Table: sales
-- ============================================================

-- 1. TOTAL REVENUE & TOTAL PROFIT
SELECT
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Revenue), 2) AS Overall_Profit_Margin_Pct
FROM sales;


-- 2. TOTAL ORDERS & TOTAL CUSTOMERS
SELECT
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    COUNT(DISTINCT Customer_ID) AS Total_Customers,
    ROUND(SUM(Revenue) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
FROM sales;


-- 3. MONTHLY SALES TREND
SELECT
    Order_Year,
    Order_Month,
    ROUND(SUM(Revenue), 2) AS Monthly_Revenue,
    ROUND(SUM(Profit), 2) AS Monthly_Profit,
    COUNT(DISTINCT Order_ID) AS Orders
FROM sales
GROUP BY Order_Year, Order_Month
ORDER BY Order_Year, Order_Month;


-- 4. QUARTERLY SALES TREND
SELECT
    Order_Year,
    Order_Quarter,
    ROUND(SUM(Revenue), 2) AS Quarterly_Revenue,
    ROUND(SUM(Profit), 2) AS Quarterly_Profit
FROM sales
GROUP BY Order_Year, Order_Quarter
ORDER BY Order_Year, Order_Quarter;


-- 5. TOP 10 PRODUCTS BY REVENUE
SELECT
    Product_Name,
    Product_Category,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Units_Sold
FROM sales
GROUP BY Product_Name, Product_Category
ORDER BY Total_Revenue DESC
LIMIT 10;


-- 6. BOTTOM 10 PRODUCTS BY REVENUE
SELECT
    Product_Name,
    Product_Category,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Units_Sold
FROM sales
GROUP BY Product_Name, Product_Category
ORDER BY Total_Revenue ASC
LIMIT 10;


-- 7. CATEGORY PERFORMANCE
SELECT
    Product_Category,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Revenue), 2) AS Profit_Margin_Pct,
    SUM(Quantity) AS Units_Sold,
    COUNT(DISTINCT Order_ID) AS Orders
FROM sales
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;


-- 8. BEST REGION (by Revenue)
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    COUNT(DISTINCT Order_ID) AS Orders,
    COUNT(DISTINCT Customer_ID) AS Customers
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC;


-- 9. WORST REGION (by Profit Margin)
SELECT
    Region,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Revenue), 2) AS Profit_Margin_Pct
FROM sales
GROUP BY Region
ORDER BY Profit_Margin_Pct ASC
LIMIT 1;


-- 10. SALES BY STATE/CITY
SELECT
    Region,
    State_City,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales
GROUP BY Region, State_City
ORDER BY Total_Revenue DESC;


-- 11. TOP 10 CUSTOMERS BY REVENUE
SELECT
    Customer_ID,
    Customer_Name,
    ROUND(SUM(Revenue), 2) AS Total_Spent,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Revenue) * 1.0 / COUNT(DISTINCT Order_ID), 2) AS Avg_Order_Value
FROM sales
GROUP BY Customer_ID, Customer_Name
ORDER BY Total_Spent DESC
LIMIT 10;


-- 12. CUSTOMER PURCHASE FREQUENCY (how many orders per customer, segmented)
SELECT
    Order_Count_Bucket,
    COUNT(*) AS Number_Of_Customers
FROM (
    SELECT
        Customer_ID,
        COUNT(DISTINCT Order_ID) AS Order_Count,
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


-- 13. NEW VS RETURNING CUSTOMERS (per year, based on first purchase year)
WITH first_purchase AS (
    SELECT
        Customer_ID,
        MIN(Order_Year) AS First_Purchase_Year
    FROM sales
    GROUP BY Customer_ID
)
SELECT
    s.Order_Year,
    SUM(CASE WHEN s.Order_Year = fp.First_Purchase_Year THEN 1 ELSE 0 END) AS New_Customer_Orders,
    SUM(CASE WHEN s.Order_Year > fp.First_Purchase_Year THEN 1 ELSE 0 END) AS Returning_Customer_Orders
FROM sales s
JOIN first_purchase fp ON s.Customer_ID = fp.Customer_ID
GROUP BY s.Order_Year
ORDER BY s.Order_Year;


-- 14. SEASONAL TRENDS (Revenue by Month across all years, to spot seasonality)
SELECT
    Order_Month,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(AVG(Revenue), 2) AS Avg_Revenue_Per_Order
FROM sales
GROUP BY Order_Month
ORDER BY Order_Month;