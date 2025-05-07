import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)

cur = conn.cursor()



with open(r"D:\taki_fair_prediction\data\processed\final_data.csv", "r", encoding="utf-8") as f:
    next(f)  # skip header
    cur.copy_expert("COPY processed_data FROM STDIN WITH CSV", f)



conn.commit()
cur.close()
conn.close()
print("Data loaded using COPY.")