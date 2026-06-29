# Business Sales Performance Analytics — Complete Code Explanation

> **File:** `sales_analysis.py`  
> **Purpose:** Generate synthetic sales data, compute KPIs, produce visualizations, and deliver actionable business recommendations.

---

## Table of Contents
1. [Libraries Used](#1-libraries-used)
2. [Section 1 — Generating Synthetic Sales Data](#2-section-1--generating-synthetic-sales-data)
3. [Section 2 — KPI Summary](#3-section-2--kpi-summary)
4. [Section 3 — Aggregations](#4-section-3--aggregations)
5. [Section 4 — Dashboard (Charts)](#5-section-4--dashboard-charts)
6. [Section 5 — Heatmap](#6-section-5--heatmap)
7. [Section 6 — Insights & Recommendations](#7-section-6--insights--recommendations)
8. [Output Files](#8-output-files)

---

## 1. Libraries Used

### `pandas` (imported as `pd`)
| Purpose | Description |
|---|---|
| Core data library | Provides the **DataFrame** — a 2D table structure like an Excel sheet in memory |
| Data manipulation | Supports filtering, grouping, sorting, pivoting, and aggregating data |
| File I/O | Read/write Excel, CSV, JSON, and more |

```python
import pandas as pd
```
**Why used here:** To store 3,000 sales transactions as a table, group by category/region, and export to Excel.

---

### `numpy` (imported as `np`)
| Purpose | Description |
|---|---|
| Numerical computing | Fast array operations, mathematical functions |
| Random number generation | Generate random integers, floats, and choices with probability weights |
| Seed control | `np.random.seed(42)` ensures reproducible random data |

```python
import numpy as np
```
**Why used here:** To randomly generate product categories, regions, prices, quantities, and discounts with realistic probability distributions.

---

### `matplotlib.pyplot` (imported as `plt`)
| Purpose | Description |
|---|---|
| Core plotting library | Creates figures, axes, line charts, bar charts, pie charts |
| Low-level control | Full control over every visual element (colors, fonts, labels, ticks) |
| File export | Save charts as PNG, PDF, SVG, etc. |

```python
import matplotlib.pyplot as plt
```
**Why used here:** To draw the monthly revenue trend line chart, horizontal bar chart for top products, and vertical bar chart for regional performance.

---

### `matplotlib.gridspec` (imported as `gridspec`)
| Purpose | Description |
|---|---|
| Layout management | Divides a figure into a grid of rows and columns |
| Span control | Allows a single chart to span multiple columns or rows |

```python
import matplotlib.gridspec as gridspec
```
**Why used here:** To create the 3×3 dashboard grid where the KPI banner spans all 3 columns and charts occupy specific grid cells.

---

### `matplotlib.patches` (imported as `mpatches`)
| Purpose | Description |
|---|---|
| Shape drawing | Add rectangles, circles, arrows, and custom shapes to plots |

```python
import matplotlib.patches as mpatches
```
**Why imported:** Available for custom legend markers or shape overlays (imported as a utility).

---

### `seaborn` (imported as `sns`)
| Purpose | Description |
|---|---|
| Statistical visualization | Higher-level charts built on top of matplotlib |
| Themes & styles | `sns.set_style()` applies clean grid backgrounds |
| Heatmaps | `sns.heatmap()` draws annotated color-coded grids |

```python
import seaborn as sns
```
**Why used here:** To set the `"whitegrid"` style for all charts and to draw the Region × Category revenue heatmap.

---

### `datetime` and `timedelta`
| Purpose | Description |
|---|---|
| `datetime` | Represents a specific date and time |
| `timedelta` | Represents a duration — used to add days to a base date |

```python
from datetime import datetime, timedelta
```
**Why used here:** To generate random transaction dates between Jan 2024 and Jun 2025 by adding random days to a start date.

---

### `warnings`
| Purpose | Description |
|---|---|
| Suppress warnings | Hides non-critical library warnings from console output |

```python
import warnings
warnings.filterwarnings('ignore')
```
**Why used here:** Keeps console output clean by suppressing matplotlib/pandas deprecation notices.

---

## 2. Section 1 — Generating Synthetic Sales Data

### `np.random.seed(42)`
```python
np.random.seed(42)
```
- **What it does:** Fixes the random number generator so every run produces the **same dataset**.
- **Why 42?** Convention — any number works; 42 is commonly used in data science examples.

---

### `np.random.choice()`
```python
cat = np.random.choice(categories, p=[0.28, 0.20, 0.18, 0.14, 0.12, 0.08])
```
- **What it does:** Randomly picks one item from a list.
- **`p=[...]`:** Probability weights — Electronics is chosen 28% of the time, Books only 8%.
- **Why:** Simulates real-world sales where Electronics outsells Books.

---

### `np.random.randint(low, high)`
```python
qty  = np.random.randint(1, 15)    # random integer between 1 and 14
days = np.random.randint(0, 548)   # random day offset over ~18 months
```
- **What it does:** Returns a random whole number between `low` (inclusive) and `high` (exclusive).

---

### `np.random.uniform(low, high)`
```python
price = round(base_prices[cat] * np.random.uniform(0.7, 1.4), 2)
```
- **What it does:** Returns a random decimal number between 0.7 and 1.4.
- **Why:** Simulates price variation (±30–40%) around the base price for each category.

---

### `timedelta(days=days)`
```python
date = start + timedelta(days=days)
```
- **What it does:** Adds a number of days to the `start` date (`2024-01-01`).
- **Result:** Produces a random transaction date spread across 18 months.

---

### `pd.DataFrame(rows, columns=[...])`
```python
df = pd.DataFrame(rows, columns=['Date','Region','Category','Product','Units_Sold','Unit_Price','Discount','Revenue'])
```
- **What it does:** Converts a plain Python list-of-lists into a structured table (DataFrame).
- **`columns`:** Names each column explicitly.

---

### `df['Date'].dt.to_period('M')`
```python
df['Month'] = df['Date'].dt.to_period('M')
```
- **`.dt`:** Accessor for datetime operations on a DataFrame column.
- **`.to_period('M')`:** Converts a full date like `2024-03-15` → `2024-03` (month period).
- **Why:** Enables monthly grouping for trend analysis.

---

### `df['Date'].dt.year`
```python
df['Year'] = df['Date'].dt.year
```
- **What it does:** Extracts just the year number (e.g., `2024`) from a date column.

---

### `df.to_excel('sales_data.xlsx', index=False)`
```python
df.to_excel('sales_data.xlsx', index=False)
```
- **What it does:** Saves the entire DataFrame to an Excel file.
- **`index=False`:** Prevents pandas from writing the row numbers (0, 1, 2…) as an extra column.

---

## 3. Section 2 — KPI Summary

### `df['Revenue'].sum()`
```python
total_rev = df['Revenue'].sum()
```
- **What it does:** Adds up all values in the `Revenue` column.
- **Result:** Total revenue across all 3,000 transactions.

---

### `df['Revenue'].mean()`
```python
avg_order = df['Revenue'].mean()
```
- **What it does:** Calculates the arithmetic average of all revenue values.

---

### `df.groupby('Category')['Revenue'].sum().idxmax()`
```python
top_cat = df.groupby('Category')['Revenue'].sum().idxmax()
```
| Step | What it does |
|---|---|
| `.groupby('Category')` | Groups rows by each unique category |
| `['Revenue']` | Selects the Revenue column within each group |
| `.sum()` | Adds up revenue per category |
| `.idxmax()` | Returns the **label** (category name) of the highest value |

---

## 4. Section 3 — Aggregations

### `df.groupby('Month')['Revenue'].sum().reset_index()`
```python
monthly_rev = df.groupby('Month')['Revenue'].sum().reset_index()
```
- **`.groupby('Month')`:** Groups all rows sharing the same month together.
- **`.sum()`:** Totals revenue per month.
- **`.reset_index()`:** Converts the grouped result back into a flat DataFrame with numbered rows (needed for plotting).

---

### `df.groupby('Product')['Revenue'].sum().nlargest(10)`
```python
prod_top10 = df.groupby('Product')['Revenue'].sum().nlargest(10).sort_values()
```
- **`.nlargest(10)`:** Keeps only the top 10 highest revenue products.
- **`.sort_values()`:** Sorts ascending (lowest to highest) — needed so the horizontal bar chart displays correctly (highest bar at top).

---

### `df.pivot_table(...)`
```python
region_cat = df.pivot_table(
    values='Revenue',
    index='Region',
    columns='Category',
    aggfunc='sum',
    fill_value=0
)
```
| Parameter | Meaning |
|---|---|
| `values='Revenue'` | The numbers to fill the table with |
| `index='Region'` | Rows = Regions |
| `columns='Category'` | Columns = Categories |
| `aggfunc='sum'` | Sum all revenue where Region + Category match |
| `fill_value=0` | Replace missing combinations with 0 instead of NaN |

- **Result:** A 5×6 grid showing total revenue for every Region–Category combination — used for the heatmap.

---

### `monthly_rev['Revenue'].pct_change() * 100`
```python
monthly_rev['MoM_Growth'] = monthly_rev['Revenue'].pct_change() * 100
```
- **`.pct_change()`:** Calculates the percentage change from the previous row.
  - Formula: $\frac{\text{current} - \text{previous}}{\text{previous}} \times 100$
- **Why:** Measures Month-over-Month (MoM) revenue growth rate.

---

## 5. Section 4 — Dashboard (Charts)

### `plt.figure(figsize=(22, 18))`
```python
fig = plt.figure(figsize=(22, 18))
```
- **What it does:** Creates a blank canvas 22 inches wide and 18 inches tall.
- **`figsize`:** Controls the physical size of the output image.

---

### `fig.patch.set_facecolor('#F0F4F8')`
```python
fig.patch.set_facecolor('#F0F4F8')
```
- **What it does:** Sets the background color of the entire figure (light blue-grey).
- **`patch`:** The rectangle that forms the figure background.

---

### `gridspec.GridSpec(3, 3, hspace=0.45, wspace=0.35)`
```python
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)
```
| Parameter | Meaning |
|---|---|
| `3, 3` | Creates a 3-row × 3-column grid |
| `hspace=0.45` | Vertical space (height) between rows |
| `wspace=0.35` | Horizontal space (width) between columns |

---

### `fig.add_subplot(gs[0, :])`
```python
ax_kpi = fig.add_subplot(gs[0, :])
```
- **`gs[0, :]`:** Row 0, **all columns** (`:` means all) → KPI banner spans full width.
- **`gs[1, :2]`:** Row 1, columns 0–1 → chart takes 2 out of 3 columns.
- **`gs[1, 2]`:** Row 1, column 2 → chart takes only 1 column.

---

### `ax.fill_between(x, y, alpha, color)`
```python
ax1.fill_between(x_idx, monthly_rev['Revenue'], alpha=0.18, color='#2196F3')
```
- **What it does:** Fills the area under the line chart with a semi-transparent color.
- **`alpha=0.18`:** Transparency (0 = fully transparent, 1 = fully opaque).
- **Why:** Creates a visually appealing area chart effect.

---

### `ax.plot(x, y, marker, color, linewidth)`
```python
ax1.plot(x_idx, monthly_rev['Revenue'], marker='o', color='#2196F3', linewidth=2.2, markersize=5)
```
- **`marker='o'`:** Draws a circle at each data point.
- **`linewidth=2.2`:** Thickness of the connecting line.
- **`markersize=5`:** Size of the circle markers.

---

### `ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: ...))`
```python
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
```
- **`FuncFormatter`:** Applies a custom function to format axis tick labels.
- **`lambda v, _`:** `v` is the tick value; `_` is the position (unused).
- **Result:** Converts raw numbers like `250000` → `$250K` on the y-axis.

---

### `ax.annotate()`
```python
ax1.annotate(f"Peak\n{monthly_rev.loc[peak_idx,'Month_str']}",
             xy=(peak_idx, monthly_rev.loc[peak_idx,'Revenue']),
             xytext=(peak_idx - 1.5, monthly_rev.loc[peak_idx,'Revenue'] * 1.05),
             arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=7)
```
| Parameter | Meaning |
|---|---|
| `xy` | The point being annotated (tip of arrow) |
| `xytext` | Where the annotation text is placed |
| `arrowprops` | Style of the arrow connecting text to point |

---

### `ax.pie(values, autopct, wedgeprops)`
```python
wedges, texts, autotexts = ax2.pie(
    cat_rev, labels=None, autopct='%1.1f%%',
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=1.5)
)
```
| Parameter | Meaning |
|---|---|
| `autopct='%1.1f%%'` | Shows percentage with 1 decimal place on each slice |
| `wedgeprops=dict(width=0.55)` | Makes it a **donut chart** — `width < 1` creates a hole |
| `startangle=140` | Rotates the first slice to 140 degrees |

---

### `ax.barh(y, width, color, height)`
```python
bars = ax3.barh(prod_top10.index, prod_top10.values, color=colors_bar, height=0.65)
```
- **`barh`:** Horizontal bar chart — categories on y-axis, values on x-axis.
- **`height=0.65`:** Bar thickness (0–1 scale).

---

### `ax.invert_yaxis()`
```python
ax3.invert_yaxis()
```
- **What it does:** Flips the y-axis so the highest-revenue product appears at the **top**.

---

### `plt.savefig('file.png', dpi=150, bbox_inches='tight')`
```python
plt.savefig('sales_dashboard.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
```
| Parameter | Meaning |
|---|---|
| `dpi=150` | Resolution — 150 dots per inch (higher = sharper image) |
| `bbox_inches='tight'` | Removes excess white space around the figure |
| `facecolor=fig.get_facecolor()` | Preserves the figure's background color in the saved file |

---

### `plt.close()`
```python
plt.close()
```
- **What it does:** Closes the current figure and frees memory.
- **Why important:** Without this, each new figure stacks on top of the old one, causing memory leaks in long scripts.

---

## 6. Section 5 — Heatmap

### `sns.set_style("whitegrid")`
```python
sns.set_style("whitegrid")
```
- **What it does:** Applies a clean white background with grey grid lines to all plots.
- **Other options:** `"darkgrid"`, `"ticks"`, `"white"`, `"dark"`.

---

### `sns.heatmap()`
```python
sns.heatmap(region_cat / 1e3, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=0.5, linecolor='white', ax=ax,
            cbar_kws={'label': 'Revenue ($ thousands)'})
```
| Parameter | Meaning |
|---|---|
| `region_cat / 1e3` | Divide all values by 1000 to display in thousands |
| `annot=True` | Print the actual number inside each cell |
| `fmt='.0f'` | Format numbers as integers (no decimal places) |
| `cmap='YlOrRd'` | Color map: Yellow → Orange → Red (low → high) |
| `linewidths=0.5` | Thin white lines between cells for readability |
| `cbar_kws` | Customizes the color scale bar label |

---

### `plt.tight_layout()`
```python
plt.tight_layout()
```
- **What it does:** Automatically adjusts subplot spacing so labels and titles don't overlap.

---

## 7. Section 6 — Insights & Recommendations

### `cat_rev.items()`
```python
for cat, rev in cat_rev.items():
    share = rev / total_rev * 100
```
- **`.items()`:** Iterates over a pandas Series as `(label, value)` pairs.
- **`share`:** Calculates each category's percentage of total revenue.

---

### `monthly_rev['MoM_Growth'].dropna().mean()`
```python
avg_growth = monthly_rev['MoM_Growth'].dropna().mean()
```
- **`.dropna()`:** Removes `NaN` values — the first month has no prior month, so MoM growth is `NaN`.
- **`.mean()`:** Averages the remaining growth percentages.

---

### `df[df['Discount'] >= 0.15]['Revenue'].sum()`
```python
high_disc = df[df['Discount'] >= 0.15]['Revenue'].sum()
```
- **`df[condition]`:** Boolean filtering — keeps only rows where `Discount >= 15%`.
- **`['Revenue'].sum()`:** Totals revenue for those filtered rows only.
- **Why:** Measures how much revenue came from heavily discounted orders.

---

## 8. Output Files

| File | How Generated | Contents |
|---|---|---|
| `sales_data.xlsx` | `df.to_excel()` | 3,000 raw transaction rows |
| `sales_dashboard.png` | `plt.savefig()` | 6-panel KPI dashboard (KPI banner + 4 charts) |
| `sales_heatmap.png` | `plt.savefig()` | Region × Category revenue heatmap |

---

## Quick Reference — Key Methods Summary

| Method | Library | What It Does |
|---|---|---|
| `pd.DataFrame()` | pandas | Creates a table from raw data |
| `df.groupby()` | pandas | Groups rows by a column value |
| `.sum()` / `.mean()` | pandas | Aggregates values |
| `.idxmax()` | pandas | Returns label of the max value |
| `.nlargest(n)` | pandas | Keeps top n values |
| `.pivot_table()` | pandas | Creates a cross-tab summary table |
| `.pct_change()` | pandas | Calculates % change row-by-row |
| `.to_excel()` | pandas | Exports DataFrame to Excel |
| `np.random.seed()` | numpy | Fixes randomness for reproducibility |
| `np.random.choice()` | numpy | Random selection with probabilities |
| `np.random.randint()` | numpy | Random integer in a range |
| `np.random.uniform()` | numpy | Random float in a range |
| `plt.figure()` | matplotlib | Creates a blank canvas |
| `fig.add_subplot()` | matplotlib | Adds a chart panel to the canvas |
| `ax.plot()` | matplotlib | Draws a line chart |
| `ax.fill_between()` | matplotlib | Fills area under a line |
| `ax.barh()` | matplotlib | Draws a horizontal bar chart |
| `ax.bar()` | matplotlib | Draws a vertical bar chart |
| `ax.pie()` | matplotlib | Draws a pie / donut chart |
| `ax.annotate()` | matplotlib | Adds labeled arrows to a chart |
| `plt.savefig()` | matplotlib | Saves chart to an image file |
| `plt.close()` | matplotlib | Frees memory after saving |
| `sns.set_style()` | seaborn | Applies a visual theme |
| `sns.heatmap()` | seaborn | Draws an annotated heatmap |
| `timedelta(days=n)` | datetime | Adds n days to a date |

---

*Generated for: Business Sales Performance Analytics — Task 1*
