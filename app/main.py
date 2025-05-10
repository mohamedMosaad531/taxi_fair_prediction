from fastapi import FastAPI
import uvicorn

from app.models.schema import PredictionRequest,PredictionResponse
from app.services.model_service import predict_fare



app=FastAPI(title="Taxi Fare Prediction API")


@app.get("/")
def root():
    # print("Root endpoint hit ")  # <-- does this show?
    return {"message": "Welcome to the Taxi Fare Prediction API"}
@app.post('/prediction',response_model=PredictionResponse)
def predict(featuress: PredictionRequest):
    fare = predict_fare(featuress)
    return PredictionResponse(fare_amount=fare)

if __name__=="__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)



