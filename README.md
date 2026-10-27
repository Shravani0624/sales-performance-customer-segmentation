# Sales Performance & Customer Segmentation

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)

**Portfolio:** https://shravani0624.github.io/portfolio/ | **Profile:** https://github.com/Shravani0624

## Data notice
**All data in this project is SYNTHETIC, generated for demonstration.**
It is not Pinevox data, not TCS data, and not any employer's real data.

## Problem
Sales teams need to know what is actually driving revenue: which months, categories, regions and channels perform, and which customers are champions, loyal, occasional or at risk, so follow-up and stock decisions are based on evidence rather than guesswork.

## Method
`analysis.py` (Python) loads the synthetic sales data and computes monthly, category, region and channel revenue, average order value, repeat-customer rate, and a rule-based RFM segmentation (Recency, Frequency, Monetary). `sql/analysis.sql` shows the same thinking in SQL: monthly aggregation, category share of total, a window-function running total, and top customers by revenue.

## Verified run results
Run with `python analysis.py` (verified October 2026):

- Orders: **1,200**
- Customers: **399**
- Total revenue: **239,369.73**
- Average order value: **199.47**
- Repeat customers: **330 (82.7%)**
- Top category: **Electronics (135,159.88)**
- Top region: **Bristol (56,429.06)**
- Best month: **2025-11 (26,776.84)**
- RFM segments: Champions **35**, Loyal **100**, Potential loyalists **35**, Occasional **120**, At risk **109**

## Limitations, stated honestly
The repeat-customer rate is high because 1,200 orders were drawn randomly across only 399 synthetic customers; it is not a real retention rate and must not be quoted as one. RFM thresholds are simple rules set on this synthetic sample, not a fitted machine-learning model, and the segments would need re-tuning on real data before any commercial use.

## How to run
```bash
pip install -r requirements.txt
python analysis.py
```

Outputs are written to `output/`: `summary_report.md`, `charts.png`, `monthly_sales.csv`, `category_sales.csv` and `rfm_segments.csv`.
