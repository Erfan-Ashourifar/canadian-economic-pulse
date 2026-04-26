import requests
import pandas as pd
import sqlite3

print("=" * 50)
print("CANADIAN ECONOMIC PULSE PIPELINE")
print("=" * 50)

# --- STEP 1: FETCH ---
print("\n[1/3] Fetching data from Bank of Canada...")

url = "https://www.bankofcanada.ca/valet/observations/ATOM_V41693242/json"
response = requests.get(url)
data = response.json()

rows = []
for item in data["observations"]:
    date = item["d"]
    value = item["ATOM_V41693242"]["v"]
    rows.append({"date": date, "inflation_rate": value})

df = pd.DataFrame(rows)
df["date"] = pd.to_datetime(df["date"])
df["inflation_rate"] = pd.to_numeric(df["inflation_rate"])
df = df.sort_values("date").tail(24)

print(f"    Fetched {len(df)} months of data.")
print(f"    Date range: {df['date'].min().strftime('%Y-%m')} to {df['date'].max().strftime('%Y-%m')}")

# --- STEP 2: SAVE TO DATABASE ---
print("\n[2/3] Saving to database...")

conn = sqlite3.connect("economic_pulse.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS inflation (
        date TEXT PRIMARY KEY,
        inflation_rate REAL
    )
""")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO inflation (date, inflation_rate)
        VALUES (?, ?)
    """, (str(row["date"].date()), row["inflation_rate"]))

conn.commit()

cursor.execute("SELECT COUNT(*) FROM inflation")
count = cursor.fetchone()[0]
print(f"    Database saved: {count} rows in economic_pulse.db")

# --- STEP 3: READ BACK AND CONFIRM ---
print("\n[3/3] Reading back from database to confirm...")

df_check = pd.read_sql("SELECT * FROM inflation ORDER BY date DESC LIMIT 5", conn)
conn.close()

print("    Latest 5 rows stored in database:")
print(df_check.to_string(index=False))

print("\n" + "=" * 50)
print("Pipeline complete!")
print("=" * 50)