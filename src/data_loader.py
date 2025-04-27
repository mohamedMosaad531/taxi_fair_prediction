import pandas as pd
from sqlalchemy import create_engine


def load_raw_data():
    engine=create_engine("postgresql://postgres:1234@localhost:5432/ml_data")
    query="Select * from raw_data"
    df=pd.read_sql(query,engine)
    return df
# print(load_raw_data())
def load_processed_data():
    engine=create_engine('postgresql://postgres:1234@localhost:5432/ml_data')
    query='Select * from data_processed '
    df=pd.read_sql(query,engine)
    return df


# print(load_raw_data())
# print('#############')
# print(load_processed_data())