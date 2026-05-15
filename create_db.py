import pandas as pd
import sqlite3

# Read CSV correctly
df_csv = pd.read_csv("fdm_1500.csv", sep=",")

# Connect database
conn = sqlite3.connect("database.db")

# Replace old wrong table
df_csv.to_sql("fdm_1500", conn, if_exists="replace", index=False)

conn.close()

print("Table created successfully")