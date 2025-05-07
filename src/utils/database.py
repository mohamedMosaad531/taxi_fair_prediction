from sqlalchemy import create_engine
import psycopg2
from src.utils.config import DB_SETTINGS


user=DB_SETTINGS["user"]
password = DB_SETTINGS["password"]
host = DB_SETTINGS["host"]
port = DB_SETTINGS["port"]
database = DB_SETTINGS["database"]


def get_sqlalchemy_engine():
       """
    Returns SQLAlchemy engine for pandas read_sql or to_sql
    """
       url=f"postgresql://{user}:{password}@{host}:{port}/{database}"
       return create_engine(url)


def get_psycog2_connection():
    """
    Returns a psycopg2 connection for COPY or raw SQL
    """
    return psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
        port=port
    )           
 