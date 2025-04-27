import psycopg2
import pandas as pd
from sqlalchemy import create_engine


data=pd.read_csv(r'D:\taki_fair_prediction\data\raw\train.csv',nrows=500000)
data.to_csv(r'D:\taki_fair_prediction\postgres\temp_data.csv',index=False)


engine=create_engine ('postgresql://postgres:1234@localhost:5432/ml_data')
data.to_sql(
    'raw_data',
    engine,
    if_exists='replace',
    index=False,
    method='multi',
    chunksize=10_000  # try 5000 or even 2000 if you still run into issues
)




# conn = psycopg2.connect("dbname=ml_data user=postgres password=1234 host=localhost port=5432")
# cur = conn.cursor()

# with open(r'D:\taki_fair_prediction\postgres\temp_data.csv', 'r', encoding='utf-8') as f:
#     cur.copy_expert("COPY raw_data FROM STDIN WITH CSV HEADER", f)


# conn.commit()
# cur.close()
# conn.close()    