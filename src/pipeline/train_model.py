from xgboost import XGBRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import root_mean_squared_error
from catboost import CatBoostRegressor

import pickle 
import joblib

import mlflow
import mlflow.sklearn
import mlflow.xgboost

def train_and_select_best(X_train,y_train,X_val,y_val):
    models={
        'XGBoost':XGBRegressor(n_estimators=300,learning_rate=.1,random_state=42),
        'Catboost':CatBoostRegressor(n_estimators=300,learning_rate=.1,random_state=42)
        
    }
    best_model=None
    best_score=float('inf')
    best_model_name=''
    mlflow.set_tracking_uri("file:///D:/taki_fair_prediction/mlruns")

    mlflow.set_experiment('taxi_fair_prediction')

    for name,model in models.items():
        with mlflow.start_run(run_name=name):
            model.fit(X_train,y_train)
            preds=model.predict(X_val)
            rmse=root_mean_squared_error(y_val,preds)
            print(f"{name} RMSE: {rmse:.4f}")
            mlflow.log_metric('rmse',rmse)
            if name == 'XGBoost':
                mlflow.xgboost.log_model(model, artifact_path='model')
            else:
                mlflow.sklearn.log_model(model, artifact_path='model')
            if rmse<best_score:
                best_score=rmse
                best_model=model
                best_model_name=name 
    print(f'Best model: {best_model_name} with RMSE: {best_score:.4f} ')      
    return best_model
def save_model(model, filename="models/production_model.pkl"):
    joblib.dump(model,filename)

