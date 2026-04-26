import sqlite3
import pandas as pd
from datetime import datetime

print("=" * 50)
print("GENERATING ECONOMIC PULSE REPORT")
print("=" * 50)

# --- CONNECT TO DATABASE ---
conn = sqlite3.connect("economic_pulse.db")

# --- READ DATA ---
df = pd.read_sql("SELECT * FROM inflation ORDER BY date ASC", conn)
conn.close()

df["date"] = pd.to_datetime(df["date"])
df["inflation_rate"] = pd.to_numeric(df["inflation_rate"])

print(f"\n[1/4] Data loaded: {len(df)} months found")

# --- CALCULATE INSIGHTS ---
print("[2/4] Calculating insights...")

latest_month     = df.iloc[-1]["date"].strftime("%B %Y")
latest_rate      = df.iloc[-1]["inflation_rate"]
previous_rate    = df.iloc[-2]["inflation_rate"]
monthly_change   = round(latest_rate - previous_rate, 2)
avg_12_months    = round(df.tail(12)["inflation_rate"].mean(), 2)
highest          = df.loc[df["inflation_rate"].idxmax()]
lowest           = df.loc[df["inflation_rate"].idxmin()]

if monthly_change > 0:
    trend = "UP"
elif monthly_change < 0:
    trend = "DOWN"
else:
    trend = "UNCHANGED"

print(f"    Latest rate  : {latest_rate}% ({latest_month})")
print(f"    Monthly trend: {trend} by {abs(monthly_change)}%")
print(f"    12-month avg : {avg_12_months}%")

# --- BUILD EXCEL REPORT ---
print("[3/4] Building Excel report...")

report_date = datetime.now().strftime("%Y-%m-%d")
filename = f"canadian_economic_pulse_{report_date}.xlsx"

writer = pd.ExcelWriter(filename, engine="openpyxl")

# Sheet 1 — Summary
summary_data = {
    "Metric": [
        "Report Date",
        "Latest Month",
        "Latest Inflation Rate",
        "Previous Month Rate",
        "Monthly Change",
        "Trend",
        "12-Month Average",
        "Highest Rate (in dataset)",
        "Highest Rate Month",
        "Lowest Rate (in dataset)",
        "Lowest Rate Month",
    ],
    "Value": [
        report_date,
        latest_month,
        f"{latest_rate}%",
        f"{previous_rate}%",
        f"{monthly_change:+.2f}%",
        trend,
        f"{avg_12_months}%",
        f"{highest['inflation_rate']}%",
        highest["date"].strftime("%B %Y"),
        f"{lowest['inflation_rate']}%",
        lowest["date"].strftime("%B %Y"),
    ]
}

df_summary = pd.DataFrame(summary_data)
df_summary.to_excel(writer, sheet_name="Summary", index=False)

# Sheet 2 — Full data
df_export = df.copy()
df_export["date"] = df_export["date"].dt.strftime("%Y-%m-%d")
df_export.columns = ["Date", "Inflation Rate (%)"]
df_export.to_excel(writer, sheet_name="Monthly Data", index=False)

# Sheet 3 — Last 12 months
df_12 = df.tail(12).copy()
df_12["date"] = df_12["date"].dt.strftime("%Y-%m-%d")
df_12["month_over_month_change"] = df_12["inflation_rate"].diff().round(2)
df_12.columns = ["Date", "Inflation Rate (%)", "Month-over-Month Change"]
df_12.to_excel(writer, sheet_name="Last 12 Months", index=False)

writer.close()

print(f"[4/4] Report saved: {filename}")
print("\n" + "=" * 50)
print("Done! Open the Excel file in your project folder.")
print("=" * 50)