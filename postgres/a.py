from sqlalchemy import create_engine
import pandas as pd

# engine = create_engine("postgresql://postgres:1234@localhost:5432/ml_data")

df=pd.read_pickle(r'D:\taki_fair_prediction\data\processed\dataframe2.pkl')
df.to_csv('temp.csv', index=False)



# with engine.connect() as conn:
#     with open('temp.csv', 'r') as f:
#         conn.connection.cursor().copy_expert(
#             "COPY data_processed FROM STDIN WITH CSV HEADER", f
#         )

# df.to_sql(
#     'data_processed',
#     engine,
#     if_exists='replace',
#     index=False,
#     method='multi',
#     chunksize=10_000  # try 5000 or even 2000 if you still run into issues
# )


import psycopg2
conn = psycopg2.connect("dbname=ml_data user=postgres password=1234 host=localhost port=5432")
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS data_processed (
    fare_amount FLOAT,
    pickup_datetime TIMESTAMP,
    pickup_longitude FLOAT,
    pickup_latitude FLOAT,
    dropoff_longitude FLOAT,
    dropoff_latitude FLOAT,
    passenger_count INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    trip_harv_dis FLOAT,
    trip_euclian_dis FLOAT,
    fare_per_km FLOAT,
    yearly_price_per_km_x FLOAT,
    monthly_price_per_km_x FLOAT,
    yearly_price_per_km_y FLOAT,
    monthly_price_per_km_y FLOAT,
    dayofweek_price_per_km FLOAT,
    hourly_price_per_km FLOAT,
    yearly_fare FLOAT,
    monthly_fare FLOAT,
    weekly_fare FLOAT,
    hourly_fare FLOAT,
    bearing FLOAT,
    manhattan_distance FLOAT,
    pickup_cluster INTEGER,
    dropoff_cluster INTEGER,
    is_night INTEGER,
    is_rush INTEGER,
    is_group INTEGER,
    jkf FLOAT,
    lga FLOAT,
    ewr FLOAT,
    met FLOAT,
    wtc FLOAT
)
""")
conn.commit()
print("Table created successfully.")

with open('temp.csv', 'r', encoding='utf-8') as f:
    cur.copy_expert("COPY data_processed FROM STDIN WITH CSV HEADER", f)


conn.commit()
cur.close()
conn.close()    