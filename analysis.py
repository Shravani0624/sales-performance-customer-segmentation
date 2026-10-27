"""Sales performance and customer segmentation analysis.

Loads the synthetic sales.csv, computes monthly, category, region and
channel summaries, and builds a rule-based RFM segmentation (Recency,
Frequency, Monetary) for customers. Charts and CSV summaries go to output/.
All data is SYNTHETIC, generated for demonstration.
"""
import csv
from collections import Counter, defaultdict
from datetime import date
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data", "sales.csv")
OUT = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

rows = list(csv.DictReader(open(DATA)))
for r in rows:
    r["quantity"] = int(r["quantity"])
    r["unit_price"] = float(r["unit_price"])
    r["revenue"] = float(r["revenue"])
    y, m, d = map(int, r["order_date"].split("-"))
    r["date"] = date(y, m, d)

total_revenue = sum(r["revenue"] for r in rows)
total_orders = len(rows)
customers = sorted(set(r["customer_id"] for r in rows))
aov = total_revenue / total_orders
repeat = sum(1 for c in customers if sum(1 for r in rows if r["customer_id"] == c) > 1)
monthly = defaultdict(float)
category = defaultdict(float)
region = defaultdict(float)
channel = defaultdict(float)
for r in rows:
    monthly[r["order_date"][:7]] += r["revenue"]
    category[r["category"]] += r["revenue"]
    region[r["region"]] += r["revenue"]
    channel[r["channel"]] += r["revenue"]
top_category = max(category, key=category.get)
top_region = max(region, key=region.get)
best_month = max(monthly, key=monthly.get)

# RFM, rule-based on quartiles of this synthetic sample only.
max_date = max(r["date"] for r in rows)
rfm = {}
for c in customers:
    cr = [r for r in rows if r["customer_id"] == c]
    recency = (max_date - max(r["date"] for r in cr)).days
    frequency = len(cr)
    monetary = sum(r["revenue"] for r in cr)
    if recency <= 30 and frequency >= 4:
        seg = "Champions"
    elif frequency >= 4:
        seg = "Loyal"
    elif recency <= 60 and monetary >= 500:
        seg = "Potential loyalists"
    elif recency > 120:
        seg = "At risk"
    else:
        seg = "Occasional"
    rfm[c] = (recency, frequency, round(monetary, 2), seg)
seg_counts = Counter(v[3] for v in rfm.values())

with open(os.path.join(OUT, "monthly_sales.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["month", "revenue"])
    for k in sorted(monthly): w.writerow([k, round(monthly[k], 2)])
with open(os.path.join(OUT, "category_sales.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["category", "revenue"])
    for k, v in sorted(category.items(), key=lambda x: -x[1]): w.writerow([k, round(v, 2)])
with open(os.path.join(OUT, "rfm_segments.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["customer_id", "recency_days", "frequency", "monetary", "segment"])
    for c in customers: w.writerow([c, *rfm[c]])

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    months = sorted(monthly); vals = [monthly[m] for m in months]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].bar(months, vals); axes[0].set_title("Monthly revenue"); axes[0].tick_params(axis="x", rotation=45)
    axes[1].bar(list(category), list(category.values())); axes[1].set_title("Revenue by category")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "charts.png")); plt.close(fig)
    charts = "charts.png created"
except Exception as e:
    charts = f"charts skipped: {e}"

report = f"""# Sales performance and customer segmentation — summary

All data is SYNTHETIC, generated for demonstration.

- Orders: {total_orders}
- Customers: {len(customers)}
- Total revenue: {total_revenue:.2f}
- Average order value: {aov:.2f}
- Repeat customers: {repeat} ({repeat/len(customers)*100:.1f}%)
- Top category: {top_category} ({category[top_category]:.2f})
- Top region: {top_region} ({region[top_region]:.2f})
- Best month: {best_month} ({monthly[best_month]:.2f})
- RFM segments: {dict(seg_counts)}
- Charts: {charts}
"""
open(os.path.join(OUT, "summary_report.md"), "w").write(report)
print(report)
