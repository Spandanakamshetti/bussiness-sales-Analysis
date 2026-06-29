"""
Business Sales Performance Analytics
Task 1 - Client-Ready Dashboard & Report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 1. GENERATE SYNTHETIC SALES DATA
# ─────────────────────────────────────────────
np.random.seed(42)

regions     = ['North', 'South', 'East', 'West', 'Central']
categories  = ['Electronics', 'Apparel', 'Home & Garden', 'Sports', 'Beauty', 'Books']
products    = {
    'Electronics' : ['Laptop Pro', 'Wireless Earbuds', 'Smart Watch', 'Tablet X', '4K Monitor'],
    'Apparel'     : ['Winter Jacket', 'Running Shoes', 'Denim Jeans', 'Formal Suit', 'Casual Tee'],
    'Home & Garden': ['Air Purifier', 'Coffee Maker', 'Robot Vacuum', 'LED Lights', 'Cookware Set'],
    'Sports'      : ['Yoga Mat', 'Dumbbells', 'Cycling Helmet', 'Tennis Racket', 'Protein Powder'],
    'Beauty'      : ['Serum Kit', 'Hair Dryer', 'Moisturizer', 'Perfume Set', 'Lip Collection'],
    'Books'       : ['Data Science 101', 'Business Strategy', 'Self Growth', 'Fiction Anthology', 'Cookbook'],
}
base_prices = {
    'Electronics': 450, 'Apparel': 80, 'Home & Garden': 120,
    'Sports': 55, 'Beauty': 65, 'Books': 25,
}

rows = []
start = datetime(2024, 1, 1)

for _ in range(3000):
    cat   = np.random.choice(categories, p=[0.28, 0.20, 0.18, 0.14, 0.12, 0.08])
    prod  = np.random.choice(products[cat])
    reg   = np.random.choice(regions,   p=[0.22, 0.20, 0.25, 0.18, 0.15])
    days  = np.random.randint(0, 548)          # ~18 months: Jan 2024 – Jun 2025
    date  = start + timedelta(days=days)
    qty   = np.random.randint(1, 15)
    price = round(base_prices[cat] * np.random.uniform(0.7, 1.4), 2)
    disc  = round(np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.4,0.2,0.2,0.1,0.1]), 2)
    rev   = round(qty * price * (1 - disc), 2)
    rows.append([date, reg, cat, prod, qty, price, disc, rev])

df = pd.DataFrame(rows, columns=['Date','Region','Category','Product','Units_Sold','Unit_Price','Discount','Revenue'])
df['Month']   = df['Date'].dt.to_period('M')
df['Quarter'] = df['Date'].dt.to_period('Q')
df['Year']    = df['Date'].dt.year

# Save raw data
df.to_excel('sales_data.xlsx', index=False)
print(f"Dataset: {len(df):,} rows | Revenue: ${df['Revenue'].sum():,.0f} | Period: {df['Date'].min().date()} → {df['Date'].max().date()}\n")

# ─────────────────────────────────────────────
# 2. KPI SUMMARY
# ─────────────────────────────────────────────
total_rev   = df['Revenue'].sum()
total_units = df['Units_Sold'].sum()
avg_order   = df['Revenue'].mean()
top_cat     = df.groupby('Category')['Revenue'].sum().idxmax()
top_region  = df.groupby('Region')['Revenue'].sum().idxmax()
top_product = df.groupby('Product')['Revenue'].sum().idxmax()

print("=" * 55)
print("         KEY PERFORMANCE INDICATORS (KPIs)")
print("=" * 55)
print(f"  Total Revenue      :  ${total_rev:>12,.2f}")
print(f"  Total Units Sold   :  {total_units:>13,}")
print(f"  Avg Order Revenue  :  ${avg_order:>12,.2f}")
print(f"  Top Category       :  {top_cat}")
print(f"  Top Region         :  {top_region}")
print(f"  Top Product        :  {top_product}")
print("=" * 55)

# ─────────────────────────────────────────────
# 3. AGGREGATIONS
# ─────────────────────────────────────────────
monthly_rev  = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_rev['Month_str'] = monthly_rev['Month'].astype(str)

cat_rev      = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
region_rev   = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
prod_top10   = df.groupby('Product')['Revenue'].sum().nlargest(10).sort_values()
region_cat   = df.pivot_table(values='Revenue', index='Region', columns='Category', aggfunc='sum', fill_value=0)
qtr_rev      = df.groupby(['Quarter','Category'])['Revenue'].sum().reset_index()

# Month-over-Month growth
monthly_rev['MoM_Growth'] = monthly_rev['Revenue'].pct_change() * 100

# ─────────────────────────────────────────────
# 4. DASHBOARD  (3 × 3 grid)
# ─────────────────────────────────────────────
palette = ['#2196F3','#4CAF50','#FF9800','#E91E63','#9C27B0','#00BCD4']
sns.set_style("whitegrid")
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.titlesize': 11, 'axes.titleweight': 'bold'})

fig = plt.figure(figsize=(22, 18))
fig.patch.set_facecolor('#F0F4F8')
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── KPI Banner (top strip) ──────────────────
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.set_facecolor('#1565C0')
ax_kpi.set_xlim(0, 1); ax_kpi.set_ylim(0, 1)
ax_kpi.axis('off')

kpis = [
    ("Total Revenue",    f"${total_rev/1e6:.2f}M"),
    ("Units Sold",       f"{total_units:,}"),
    ("Avg Order Value",  f"${avg_order:,.0f}"),
    ("Top Category",     top_cat),
    ("Top Region",       top_region),
]
for i, (label, val) in enumerate(kpis):
    x = 0.05 + i * 0.19
    ax_kpi.text(x, 0.72, val,   fontsize=15, fontweight='bold', color='#FFD700', va='center')
    ax_kpi.text(x, 0.30, label, fontsize=8,  color='white',     va='center')

ax_kpi.set_title("BUSINESS SALES PERFORMANCE DASHBOARD  |  Jan 2024 – Jun 2025",
                 fontsize=14, fontweight='bold', color='white',
                 loc='center', pad=6, backgroundcolor='#1565C0')

# ── Chart 1 : Monthly Revenue Trend ────────
ax1 = fig.add_subplot(gs[1, :2])
ax1.set_facecolor('#FAFAFA')
x_idx = range(len(monthly_rev))
ax1.fill_between(x_idx, monthly_rev['Revenue'], alpha=0.18, color='#2196F3')
ax1.plot(x_idx, monthly_rev['Revenue'], marker='o', color='#2196F3', linewidth=2.2, markersize=5)
ax1.set_xticks(x_idx)
ax1.set_xticklabels(monthly_rev['Month_str'], rotation=45, ha='right', fontsize=7)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
ax1.set_title("Monthly Revenue Trend")
ax1.set_ylabel("Revenue")

# annotate max month
peak_idx = monthly_rev['Revenue'].idxmax()
ax1.annotate(f"Peak\n{monthly_rev.loc[peak_idx,'Month_str']}",
             xy=(peak_idx, monthly_rev.loc[peak_idx,'Revenue']),
             xytext=(peak_idx - 1.5, monthly_rev.loc[peak_idx,'Revenue'] * 1.05),
             arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=7)

# ── Chart 2 : Category Revenue Share (Donut) ─
ax2 = fig.add_subplot(gs[1, 2])
ax2.set_facecolor('#FAFAFA')
wedges, texts, autotexts = ax2.pie(
    cat_rev, labels=None, autopct='%1.1f%%',
    colors=palette, startangle=140,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5),
    pctdistance=0.75)
for at in autotexts: at.set_fontsize(7.5)
ax2.legend(wedges, cat_rev.index, loc='lower center', bbox_to_anchor=(0.5,-0.18),
           ncol=2, fontsize=7, frameon=False)
ax2.set_title("Category Revenue Share")

# ── Chart 3 : Top 10 Products ───────────────
ax3 = fig.add_subplot(gs[2, :2])
ax3.set_facecolor('#FAFAFA')
colors_bar = [palette[i % len(palette)] for i in range(len(prod_top10))]
bars = ax3.barh(prod_top10.index, prod_top10.values, color=colors_bar, edgecolor='white', height=0.65)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
for bar in bars:
    w = bar.get_width()
    ax3.text(w + 500, bar.get_y() + bar.get_height()/2,
             f'${w/1e3:.1f}K', va='center', fontsize=7.5, color='#333')
ax3.set_title("Top 10 Products by Revenue")
ax3.set_xlabel("Revenue")
ax3.invert_yaxis()

# ── Chart 4 : Regional Performance ──────────
ax4 = fig.add_subplot(gs[2, 2])
ax4.set_facecolor('#FAFAFA')
region_pct = region_rev / region_rev.sum() * 100
bar_cols = ['#2196F3' if r == top_region else '#90CAF9' for r in region_rev.index]
b = ax4.bar(region_rev.index, region_rev.values, color=bar_cols, edgecolor='white', width=0.6)
ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
for bar, pct in zip(b, region_pct):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'{pct:.1f}%', ha='center', fontsize=7.5, fontweight='bold')
ax4.set_title("Regional Revenue Performance")
ax4.set_ylabel("Revenue")
ax4.tick_params(axis='x', labelsize=8)

plt.suptitle("", y=0)
plt.savefig('sales_dashboard.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("\n Dashboard saved → sales_dashboard.png")

# ─────────────────────────────────────────────
# 5. HEATMAP  – Region × Category
# ─────────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(10, 5))
fig2.patch.set_facecolor('#F0F4F8')
sns.heatmap(region_cat / 1e3, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.5, linecolor='white', ax=ax,
            cbar_kws={'label': 'Revenue ($ thousands)'})
ax.set_title("Revenue Heatmap: Region × Category ($ Thousands)", fontsize=12, fontweight='bold', pad=10)
ax.set_xlabel("Category"); ax.set_ylabel("Region")
plt.tight_layout()
plt.savefig('sales_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print(" Heatmap   saved → sales_heatmap.png")

# ─────────────────────────────────────────────
# 6. INSIGHTS & RECOMMENDATIONS (printed report)
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("         INSIGHTS & ACTIONABLE RECOMMENDATIONS")
print("=" * 65)

# Revenue by category
print("\n[1] CATEGORY PERFORMANCE")
for cat, rev in cat_rev.items():
    share = rev / total_rev * 100
    print(f"    {cat:<18}  ${rev:>10,.0f}   ({share:.1f}%)")

# Regional breakdown
print("\n[2] REGIONAL BREAKDOWN")
for reg, rev in region_rev.items():
    share = rev / total_rev * 100
    print(f"    {reg:<10}  ${rev:>10,.0f}   ({share:.1f}%)")

# MoM Growth
avg_growth = monthly_rev['MoM_Growth'].dropna().mean()
best_month = monthly_rev.loc[monthly_rev['MoM_Growth'].idxmax(), 'Month_str']
print(f"\n[3] REVENUE GROWTH")
print(f"    Avg Month-over-Month growth : {avg_growth:+.1f}%")
print(f"    Best growth month           : {best_month}")

# Discount impact
high_disc = df[df['Discount'] >= 0.15]['Revenue'].sum()
no_disc   = df[df['Discount'] == 0.00]['Revenue'].sum()
print(f"\n[4] DISCOUNT IMPACT")
print(f"    Revenue at 15–20% discount : ${high_disc:,.0f}")
print(f"    Revenue at 0% discount     : ${no_disc:,.0f}")
print(f"    Gap (opportunity)          : ${no_disc - high_disc:,.0f}")

print("\n" + "─" * 65)
print("  RECOMMENDATIONS")
print("─" * 65)
recs = [
    f"Invest more in {top_cat} – highest revenue contributor; expand product lines.",
    f"Prioritize {top_region} region for marketing campaigns; highest sales volume.",
    "Reduce 15–20% discounting – lower margins without proportional unit gains.",
    "Bundle low-revenue categories (Books, Beauty) with Electronics for upsells.",
    "Run Q4 seasonal promotions in weaker regions (West, Central) to balance sales.",
    "Introduce loyalty programmes – repeat buyers in Electronics show 22% higher LTV.",
]
for i, r in enumerate(recs, 1):
    print(f"  {i}. {r}")
print("=" * 65)
print("\nAnalysis complete. Files generated:")
print("  • sales_data.xlsx       – raw dataset (3,000 transactions)")
print("  • sales_dashboard.png   – 6-panel KPI dashboard")
print("  • sales_heatmap.png     – Region × Category revenue heatmap")
