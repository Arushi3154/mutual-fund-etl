import sqlite3
import pandas as pd
import os

os.makedirs("powerbi_data", exist_ok=True)
conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]

print(f"📦 Found {len(tables)} tables in database:")
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    file_path = f"powerbi_data/{table}.csv"
    df.to_csv(file_path, index=False)
    print(f"  └─ Exported {table} ({len(df):,} rows) -> {file_path}")

conn.close()
print("\n✅ Power BI data directory ready: ./powerbi_data/")
