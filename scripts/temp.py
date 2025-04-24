import numpy as np
import pickle
import pandas as pd
from datetime import datetime
import pytz


loaded_model=pickle.load(open('D:/taki_fair_prediction/models/trained_model_xgboost.sav','rb'))

kmeans=pickle.load(open('D:/taki_fair_prediction/models/cluster_model.sav','rb'))

prediction=loaded_model.predict([[4,2013,3,20,2.904737,	0.028262,0.039451,4.08,	10.75,28.605989,12,0,0,1,-73.995145,40.760157,-73.978627,40.783090]])
# print(loaded_model)
# print(prediction)
yearly_fare=pd.read_pickle(r'D:\taki_fair_prediction\data\processed\temp\yearly_fare.pkl')
hourly_fare=pd.read_pickle(r'D:\taki_fair_prediction\data\processed\temp\hourly_fare.pkl')
monthly_price_per_km=pd.read_pickle(r'D:\taki_fair_prediction\data\processed\temp\monthly_price_per_km.pkl')
yearly_price_per_km=pd.read_pickle(r'D:\taki_fair_prediction\data\processed\temp\yearly_price_per_km.pkl')

def processing(key,pickup_datetime,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count):
    test_df={'key':key,'pickup_datetime':pickup_datetime,'pickup_longitude':pickup_longitude,'pickup_latitude':pickup_latitude,'dropoff_longitude':dropoff_longitude,
             'dropoff_latitude':dropoff_latitude,'passenger_count':passenger_count}
    test_df= pd.DataFrame(test_df,index=[0])
    # pickup_dt = datetime.strptime(pickup_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
    # dropoff_dt = datetime.strptime(dropoff_str, "%Y-%m-%d %H:%M:%S %Z")

    # # If UTC needed:
    # dropoff_dt = dropoff_dt.replace(tzinfo=pytz.UTC)

    test_df['pickup_datetime'] = pd.to_datetime(test_df['pickup_datetime'])

    test_df['key']=pd.to_datetime(test_df['key'])
    test_df['year']=test_df['key'].dt.year
    test_df['month']=test_df['key'].dt.month
    test_df['day']=test_df['key'].dt.month

    test_df['hour']=test_df['key'].dt.hour

    test_df=test_df.merge(yearly_fare,on='year',how='left')
    test_df=test_df.merge(hourly_fare,on='hour',how='left')
    test_df=test_df.merge(monthly_price_per_km,on='month',how='left')
    test_df=test_df.merge(yearly_price_per_km,on='year',how='left')

    def harvesine_dis(lon1,lat1,lon2,lat2):
        R = 6371  # Earth radius in kilometers

        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c

    def euclidean_distance(lon1, lat1, lon2, lat2):
        return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

    def add_dis(df):
        df["trip_harv_dis"]=harvesine_dis(df.pickup_longitude, df.pickup_latitude, df.dropoff_longitude, df.dropoff_latitude)
        df["trip_euclian_dis"]=euclidean_distance(df.pickup_longitude, df.pickup_latitude, df.dropoff_longitude, df.dropoff_latitude)

    add_dis(test_df)


    test_df.rename(columns={"monthly_price_per_km": "monthly_price_per_km_x"}, inplace=True)
    test_df.rename(columns={"yearly_price_per_km": "yearly_price_per_km_x"}, inplace=True)

    def calculate_bearing(pickup_lat, pickup_long, dropoff_lat, dropoff_long):
        delta_lon = np.radians(dropoff_long - pickup_long)
        pickup_lat = np.radians(pickup_lat)
        dropoff_lat = np.radians(dropoff_lat)

        x = np.sin(delta_lon) * np.cos(dropoff_lat)
        y = np.cos(pickup_lat) * np.sin(dropoff_lat) - \
            np.sin(pickup_lat) * np.cos(dropoff_lat) * np.cos(delta_lon)
        bearing = np.arctan2(x, y)
        return np.degrees(bearing) % 360
    def add_bearing(df):
        df["bearing"]=calculate_bearing( df.pickup_latitude,df.pickup_longitude, df.dropoff_latitude, df.dropoff_longitude)


    def manhattan_distance(df):
        df['manhattan_distance']=np.abs(df['dropoff_latitude']-df['pickup_latitude'])+np.abs(df['dropoff_longitude']-df['pickup_longitude'])
    manhattan_distance(test_df)
    add_bearing(test_df)
    test_df['pickup_cluster']=kmeans.predict(test_df[['pickup_latitude','pickup_longitude']])

    temp_long_lat=test_df[['dropoff_latitude','dropoff_longitude']]
    temp_long_lat.columns=['pickup_latitude','pickup_longitude']


    test_df['dropoff_cluster']=kmeans.predict(temp_long_lat)


    test_df['is_night']=test_df['hour'].isin([0,1,2,3,4])
    test_df['is_rush']=test_df['hour'].isin([8,9,15,16,17,18,19])
    test_df['is_group'] = test_df['passenger_count'] > 1


    features=['passenger_count',
    'year',
    'month',
    'hour',
    'trip_harv_dis',
    'trip_euclian_dis',
    'manhattan_distance',
    'yearly_price_per_km_x',
    'hourly_fare',
    'bearing',
    'pickup_cluster',
    'is_night',
    'is_rush',
    'is_group',
    'pickup_longitude',
    'pickup_latitude',
    'dropoff_longitude',
    'dropoff_latitude']
    return test_df[features]


pickup_str = "2015-01-27 13:08:24.0000003"
dropoff_str = "2015-01-27 13:08:24 UTC"




# Now call the function
a=processing(pickup_str, dropoff_str,
           -73.986862182617188, 40.719383239746094,
           -73.998886108398438, 40.739200592041016,
           1)
# print(a)
# print(yearly_fare)