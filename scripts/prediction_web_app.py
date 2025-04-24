import numpy as np
import pickle
import streamlit as st
from temp import processing

loaded_model=pickle.load(open('D:/taki_fair_prediction/models/trained_model_xgboost.sav','rb'))
print('aa')

def main():
    #giving a title
    st.title('Taxi Fair Prediction in New York')


    #getting the input data

    key=st.text_input('Key')
    pickup_datetime=st.text_input('Pickup Datetime')
    pickup_longitude=st.number_input('Pickup Longitude')
    pickup_latitude=st.number_input('Pickup Latitude')
    dropoff_longitude=st.number_input('Dropoff Longitude')
    dropoff_latitude=st.number_input('Dropoff Latitude')
    passenger_count=st.number_input('Passenger Count')

    #crating a button for prediction
    data_after_FE=processing(key,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count)

    if st.button('Taxi Fair Prediction'):
        prediction=loaded_model.predict(data_after_FE)

        st.success(prediction)


if __name__=='__main__':
    main()