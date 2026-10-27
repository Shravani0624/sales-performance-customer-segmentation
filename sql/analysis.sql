-- Sales analysis in SQL: monthly trend, category and region share,
-- top customers, and a window-function running total.
-- Load data/sales.csv into a sales table first (SQLite .import or equivalent).

-- Monthly revenue
SELECT substr(order_date, 1, 7) AS month,
       COUNT(*) AS orders,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY month
ORDER BY month;

-- Revenue by category, with share of total
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM sales), 1) AS pct_of_total
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Running monthly total (window function)
WITH monthly AS (
  SELECT substr(order_date, 1, 7) AS month, SUM(revenue) AS revenue
  FROM sales GROUP BY month
)
SELECT month, ROUND(revenue, 2) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY month), 2) AS running_total
FROM monthly
ORDER BY month;

-- Top 10 customers by revenue, with order count
SELECT customer_id,
       COUNT(*) AS orders,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 10;
