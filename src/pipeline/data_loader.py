import pandas as pd
from sqlalchemy import create_engine
from  src.utils.database import get_sqlalchemy_engine

def load_raw_data():
    engine=get_sqlalchemy_engine()
    query="Select * from new_data limit 500000"
    df=pd.read_sql(query,engine)
    return df
# print(load_raw_data())
def load_processed_data():
    engine=get_sqlalchemy_engine()
    query='Select * from processed_data '
    df=pd.read_sql(query,engine)
    return df


# print(load_raw_data())
# print('#############')
# print(load_processed_data())