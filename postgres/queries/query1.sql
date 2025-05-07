-- Active: 1746554608701@@localhost@5432@ml_data
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'processed_data';


-- ALTER TABLE processed_data ADD COLUMN fare_amount FLOAT;
