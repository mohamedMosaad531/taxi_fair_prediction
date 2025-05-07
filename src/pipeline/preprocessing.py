import pandas as pd
import numpy as np
import pickle
from src.pipeline.data_loader import load_raw_data
from src.utils.config import FILE_PATHS

yearly_fare = pd.read_pickle(FILE_PATHS["yearly_fare"])
hourly_fare = pd.read_pickle(FILE_PATHS["hourly_fare"])
monthly_price_per_km = pd.read_pickle(FILE_PATHS["monthly_price_per_km"])
yearly_price_per_km = pd.read_pickle(FILE_PATHS["yearly_price_per_km"])


JFK_LONLAT = -73.7781, 40.6413
LGA_LONLAT = -73.8740, 40.7769
EWR_LONLAT = -74.1745, 40.6895
MET_LONLAT = -73.9632, 40.7794
WTC_LONLAT = -74.0099, 40.7126


kmeans=pickle.load(open('D:/taki_fair_prediction/models/cluster_model.sav','rb'))


def preprocess(df):
    df.dropna(inplace=True)
    min_longitude=-76#-74.26
    max_longitude=-71#-73.70
    min_latitude= 39#40.49
    max_latitude=42#40.92
    mask=(
    (df['pickup_longitude']> max_longitude) | ( df['pickup_longitude']<min_longitude) |
   (df["pickup_latitude"]<min_latitude) | (df['pickup_latitude']>max_latitude ) |
    (df['dropoff_latitude']>max_latitude)  | ( df["dropoff_latitude"]<min_latitude) |
     (df["dropoff_longitude"]<min_longitude) | (df["dropoff_longitude"]>max_longitude)
    )
    df=df[~mask].copy()

    df=df[(df["fare_amount"]<200 )& (df["fare_amount"]>.5)]
       
    df=df[df['passenger_count'].isin([1,2,3,4,5,6])].copy() 

    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

    df['key']=pd.to_datetime(df['key'])
    df['year']=df['key'].dt.year
    df['month']=df['key'].dt.month
    df['day']=df['key'].dt.day

    df['hour']=df['key'].dt.hour
    # df['minute']=df['minute'].dt.minute

    df=df.merge(yearly_fare,on='year',how='left')
    df=df.merge(hourly_fare,on='hour',how='left')
    df=df.merge(monthly_price_per_km,on='month',how='left')
    df=df.merge(yearly_price_per_km,on='year',how='left')

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

    add_dis(df)
    df=df[(df['trip_harv_dis']<50) &(df['trip_harv_dis']!=0) ].copy()

     
    df.rename(columns={"monthly_price_per_km": "monthly_price_per_km_x"}, inplace=True)
    df.rename(columns={"yearly_price_per_km": "yearly_price_per_km_x"}, inplace=True)

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
    manhattan_distance(df)
    add_bearing(df)
    df['pickup_cluster']=kmeans.predict(df[['pickup_latitude','pickup_longitude']])

    temp_long_lat=df[['dropoff_latitude','dropoff_longitude']]
    temp_long_lat.columns=['pickup_latitude','pickup_longitude']


    df['dropoff_cluster']=kmeans.predict(temp_long_lat)


    df['is_night']=df['hour'].isin([0,1,2,3,4])
    df['is_rush']=df['hour'].isin([8,9,15,16,17,18,19])
    df['is_group'] = df['passenger_count'] > 1
    df['jkf']=abs(df['dropoff_latitude']-JFK_LONLAT[1])+abs(df['dropoff_longitude']-JFK_LONLAT[0])
    df['lga']=abs(df['dropoff_latitude']-LGA_LONLAT[1])+abs(df['dropoff_longitude']-LGA_LONLAT[0])
    df['ewr']=abs(df['dropoff_latitude']-EWR_LONLAT[1])+abs(df['dropoff_longitude']-EWR_LONLAT[0])
    df['met']=abs(df['dropoff_latitude']-MET_LONLAT[1])+abs(df['dropoff_longitude']-MET_LONLAT[0])
    df['wtc']=abs(df['dropoff_latitude']-WTC_LONLAT[1])+abs(df['dropoff_longitude']-WTC_LONLAT[0])

    # features=['passenger_count',
    # 'year','month','hour',
    # 'trip_harv_dis',
    # 'trip_euclian_dis',
    # 'manhattan_distance',
    # 'yearly_price_per_km_x',
    # 'hourly_fare',
    # 'bearing',
    # 'pickup_cluster',
    # 'is_night','is_rush','is_group',
    # 'pickup_longitude','pickup_latitude',
    # 'dropoff_longitude','dropoff_latitude',
    # 'jkf','lga','ewr','met','wtc']
    return df

# aa=load_raw_data()
# bb=preprocess(aa)

# print(bb.columns)
