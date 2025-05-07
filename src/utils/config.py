from dotenv import load_dotenv
import os

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path)

DB_SETTINGS = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DB")
}


DATA_DIR = os.getenv("DATA_DIR")

FILE_PATHS = {
    "yearly_fare": os.path.join(DATA_DIR, "yearly_fare.pkl"),
    "hourly_fare": os.path.join(DATA_DIR, "hourly_fare.pkl"),
    "monthly_price_per_km": os.path.join(DATA_DIR, "monthly_price_per_km.pkl"),
    "yearly_price_per_km": os.path.join(DATA_DIR, "yearly_price_per_km.pkl"),
}
 
FEATURES = [
    'passenger_count',
    'year', 'month', 'hour',
    'trip_harv_dis',
    'trip_euclian_dis',
    'manhattan_distance',
    'yearly_price_per_km_x',
    'hourly_fare',
    'bearing',
    'pickup_cluster',
    'is_night', 'is_rush', 'is_group',
    'pickup_longitude', 'pickup_latitude',
    'dropoff_longitude', 'dropoff_latitude',
    'jkf', 'lga', 'ewr', 'met', 'wtc'
]