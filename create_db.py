import pandas as pd
import sqlite3

# Read CSV correctly
df_csv = pd.read_csv("Dataset.csv")

# Connect database
conn = sqlite3.connect("database.db")

# Create table
df_csv.to_sql(
    name="sales_data",
    con=conn,
    if_exists="replace",
    index=False
)
conn.close()

print("Table created successfully")