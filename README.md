# 🛒 Retail Sales & Customer Insights Dashboard

An end-to-end data analytics project that transforms raw retail transaction data into actionable business insights using **SQL**, **Python**, and **Power BI**.

---

## 📌 Project Overview

This project simulates a real-world retail analytics scenario where a company needs to understand its sales performance, customer behavior, product trends, and regional growth opportunities.

The goal was to build a complete analytics pipeline — from raw messy data to an interactive dashboard — that demonstrates the core skills expected for **Data Analyst**, **Business Analyst**, and **Technology Analyst** roles.

---

## 🎯 Business Problem

A retail company has years of transaction data but no clear visibility into:
- Which products and categories drive the most revenue and profit?
- Which regions and cities are performing best?
- Who are the top customers and how loyal are they?
- What are the seasonal and monthly sales trends?
- Where are the opportunities to improve profitability?

This dashboard answers all of these questions.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy, Matplotlib) | Data generation, cleaning, EDA |
| SQLite + SQL | Database storage and business queries |
| Power BI | Interactive dashboard and visualizations |
| Git & GitHub | Version control and project management |

---

## 📂 Project Structure

```
Retail-Sales-Dashboard/
│
├── dataset/
│   ├── retail_sales_raw.csv        # Raw synthetic dataset (8,160 rows)
│   └── retail_sales_clean.csv      # Cleaned dataset (8,007 rows, 18 columns)
│
├── sql/
│   ├── analysis_queries.sql        # 14 business SQL queries
│   └── retail_sales.db             # SQLite database
│
├── python/
│   ├── generate_dataset.py         # Synthetic data generation script
│   ├── clean_data.py               # Data cleaning script
│   ├── load_to_sql.py              # Load data into SQLite
│   ├── run_sql_analysis.py         # Run SQL queries via Python
│   └── eda_visualization.py        # EDA charts with Matplotlib
│
├── powerbi/
│   └── Retail_Sales_Dashboard.pbix # Power BI dashboard file
│
├── screenshots/                    # EDA chart images
├── INSIGHTS.md                     # Business insights & recommendations
├── LICENSE
└── README.md
```

---

## 📊 Dataset

- **8,007 records** after cleaning (from 8,160 raw)
- **18 columns** including Order ID, Customer ID/Name, Product Name/Category, Quantity, Unit Price, Revenue, Profit, Order Date, Region, State/City, and calculated columns
- **3 years** of data (2023–2025)
- **1,776 unique customers** across 4 regions (North, South, East, West)
- **7 product categories:** Electronics, Furniture, Clothing, Groceries, Home Decor, Sports, Stationery

### Data Cleaning Performed
- ✅ Removed 153 duplicate rows
- ✅ Standardized 4 different date formats into YYYY-MM-DD
- ✅ Fixed inconsistent category names (electronics/ELECTRONICS/Electronic → Electronics)
- ✅ Filled missing Customer Names and Regions using Customer ID lookup
- ✅ Recalculated missing Unit Prices from Revenue ÷ Quantity
- ✅ Added calculated columns: Profit Margin %, Revenue Per Customer, Avg Order Value

---

## 🗄 SQL Analysis

14 business queries covering:
- Total Revenue, Profit, and Margin
- Monthly and Quarterly Sales Trends
- Top 10 & Bottom 10 Products
- Category Performance
- Best & Worst Regions
- Top 10 Customers by Revenue
- Customer Purchase Frequency Segmentation
- New vs Returning Customer Analysis
- Seasonal Trends

---

## 📈 Power BI Dashboard

**5-page interactive dashboard:**

| Page | Content |
|------|---------|
| Overview | 6 KPI cards + Monthly Trend + Category & Region charts |
| Sales Analysis | Monthly/Quarterly/Yearly revenue & profit trends |
| Product Analysis | Top 10 products, Revenue & Profit by Category |
| Regional Analysis | Revenue & Profit by Region and City |
| Customer Analysis | Top customers, purchase frequency, monthly activity |

**Interactive filters:** Year, Region, Product Category

---

## 💡 Key Insights

- **West region** leads in revenue (₹123.2M) and order volume
- **Electronics** has the highest profit margin (20.99%)
- **Stationery** dominates top products — Desk Organizer is #1
- **49% of customers** are repeat buyers (4–6 orders) — strong loyalty
- Overall profit margin is a healthy **20.09%** across all categories

→ See [INSIGHTS.md](INSIGHTS.md) for full analysis and recommendations

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/ANKAN-22/Retail-Sales-Dashboard.git
cd Retail-Sales-Dashboard
```

### 2. Install Python dependencies
```bash
pip install pandas numpy faker matplotlib
```

### 3. Run the pipeline
```bash
cd python
python generate_dataset.py    # Generate raw dataset
python clean_data.py          # Clean the data
python load_to_sql.py         # Load into SQLite
python run_sql_analysis.py    # Run SQL analysis
python eda_visualization.py   # Generate EDA charts
```

### 4. Open the dashboard
Open `powerbi/Retail_Sales_Dashboard.pbix` in Power BI Desktop

---

## 🎤 Project Summary

This project demonstrates a complete retail analytics pipeline — from raw data 
generation and cleaning, through SQL analysis and Python EDA, to an interactive 
5-page Power BI dashboard. It covers 8,000+ transactions across 3 years, 4 regions, 
and 7 product categories, with business insights and recommendations derived directly 
from the data.

---

## 👨‍💻 Skills Demonstrated

`SQL` `Python` `Pandas` `Data Cleaning` `Data Analysis` `Power BI` `Data Visualization` `Business Intelligence` `Data Storytelling` `GitHub`

---

*Built as a portfolio project to demonstrate data analyst skills for internship and entry-level roles.*