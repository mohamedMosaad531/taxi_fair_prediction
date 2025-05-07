-- Active: 1746491373511@@127.0.0.1@5432@ml_data
CREATE TABLE IF NOT EXISTS processed_data (
    passenger_count INTEGER,
    year INTEGER,
    month INTEGER,
    hour INTEGER,
    trip_harv_dis DOUBLE PRECISION,
    trip_euclian_dis DOUBLE PRECISION,
    manhattan_distance DOUBLE PRECISION,
    yearly_price_per_km_x DOUBLE PRECISION,
    hourly_fare DOUBLE PRECISION,
    bearing DOUBLE PRECISION,
    pickup_cluster INTEGER,
    is_night BOOLEAN,
    is_rush BOOLEAN,
    is_group BOOLEAN,
    pickup_longitude DOUBLE PRECISION,
    pickup_latitude DOUBLE PRECISION,
    dropoff_longitude DOUBLE PRECISION,
    dropoff_latitude DOUBLE PRECISION,
    jkf DOUBLE PRECISION,
    lga DOUBLE PRECISION,
    ewr DOUBLE PRECISION,
    met DOUBLE PRECISION,
    wtc DOUBLE PRECISION,
    fare_amount DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS new_data(
    key TEXT ,
    fare_amount DOUBLE PRECISION,
    pickup_datetime TIMESTAMP,
    pickup_longitude DOUBLE PRECISION,
    pickup_latitude DOUBLE PRECISION,
    dropoff_longitude DOUBLE PRECISION,
    dropoff_latitude DOUBLE PRECISION,
    passenger_count INTEGER
);



-- COPY processed_data FROM '/data/processed/final_data.csv' DELIMITER ',' CSV HEADER;
-- COPY new_data FROM '/data/new_data/new_data.csv' DELIMITER ',' CSV HEADER;
