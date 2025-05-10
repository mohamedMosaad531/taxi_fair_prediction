# Use a slim Python image to reduce the image size
FROM python:3.11-slim

# Set a working directory in the container
WORKDIR /app

# Set the environment variable DATA_DIR to point to the directory where the files will be located inside the container
ENV DATA_DIR=/app/data/processed/temp

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY models/ .

# Copy the data directory containing the necessary pickle files into the container
COPY data/processed/temp /app/data/processed/temp

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
