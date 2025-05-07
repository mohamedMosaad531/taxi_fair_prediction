from src.pipeline.data_loader import load_raw_data,load_processed_data
from src.utils.config import FEATURES

from src.pipeline.preprocessing import preprocess
from src.pipeline.train_model import train_and_select_best,save_model
from sklearn.model_selection import train_test_split
import pandas as pd

def retrain():
    print("[INFO] Loading data...")
    df1=load_raw_data()
    df2=load_processed_data()

    print('[INFO] preprocessing data...')
    df1=preprocess(df1)



    X1=df1[FEATURES]
    y1=df1['fare_amount']

    X2=df2[FEATURES]
    y2=df2['fare_amount']

    X = pd.concat([X1, X2], axis=0)
    y=pd.concat([y1,y2],axis=0)

    print("[INFO] Splitting data...")
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=42)

    print("[INFO] Training model...")
    model = train_and_select_best(X_train, y_train,X_test,y_test)

    print("[INFO] Saving model...")
    save_model(model)

    print("[SUCCESS] Retraining complete. Model saved.")


if __name__=="__main__":
    retrain()