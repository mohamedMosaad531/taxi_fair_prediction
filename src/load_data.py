import psycopg2
import os
from dotenv import load_dotenv
from src.utils.database import get_psycog2_connection 
load_dotenv()

conn = get_psycog2_connection()

cur = conn.cursor()

with open(r"D:\taki_fair_prediction\data\new_data\new_data.csv", "r", encoding="utf-8") as f:
    next(f)  # skip header
    cur.copy_expert("COPY new_data FROM STDIN WITH CSV", f)

conn.commit()
cur.close()
conn.close()
# print(" Data loaded using COPY.")







