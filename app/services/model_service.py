import numpy as np
import pandas as pd


from app.models.schema import PredictionRequest
from app.utils.load_model import get_model

from src.pipeline.preprocessing import preprocess_input
from src.utils.config import FEATURES

model = get_model()

def  predict_fare(request:PredictionRequest)  ->float:
    data = pd.DataFrame([{
        "key":request.key,
        "pickup_datetime": request.pickup_datetime,
        "pickup_latitude": request.pickup_latitude,
        "pickup_longitude": request.pickup_longitude,
        "dropoff_longitude": request.dropoff_longitude,
        "dropoff_latitude": request.dropoff_latitude,
        "passenger_count": request.passenger_count
    }])
    processed_features=preprocess_input(data)[FEATURES]
    return model.predict(processed_features)[0]
