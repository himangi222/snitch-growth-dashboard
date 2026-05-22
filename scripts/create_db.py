import sqlite3
import pandas as pd

conn = sqlite3.connect("data/snitch.db")

catalog = pd.read_csv("data/snitch_catalog.csv")
funnel = pd.read_csv("data/funnel_data.csv")

catalog.to_sql("catalog", conn, if_exists="replace", index=False)
funnel.to_sql("funnel", conn, if_exists="replace", index=False)

print("Database Created!")