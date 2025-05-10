from pydantic import BaseModel 

class PredictionRequest(BaseModel):
    key:str
    pickup_datetime:str
    pickup_longitude:float
    pickup_latitude:float
    dropoff_longitude:float
    dropoff_latitude:float
    passenger_count:int


class PredictionResponse(BaseModel):
    fare_amount: float
