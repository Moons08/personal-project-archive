'''
need to install holidays
pip install holidays

https://github.com/dr-prodigy/python-holidays
'''

import numpy as np
import pandas as pd
import datetime as dt
import holidays

from taxi_pakage import haversine_np

datezero = dt.datetime(2016, 1, 1, 0, 0, 1) # 기준

def strptime(x):
    return dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
def date_to_zero(x):
    return int((x-datezero).days)
def time_to_zero(x):
    return int((x-datezero).seconds)
def week_num(x):
    return int(x.weekday())

us_holidays = holidays.US(state='NY', years=2016)

def holiday(x):
    if x in us_holidays:
        return 1
    else:
        x = x.weekday()
    if x > 4:
        return 0
    else:
        return 0


taxi = pd.read_csv('test.csv')
taxi['store_and_fwd_flag'] = taxi['store_and_fwd_flag'].apply(lambda x: 0 if x == 'N' else 1)

taxi['dist'] = haversine_np(taxi['pickup_longitude'], taxi['pickup_latitude'], taxi['dropoff_longitude'], taxi['dropoff_latitude'])

taxi['pickup_datetime'] = taxi['pickup_datetime'].apply(strptime)
taxi["month"] = taxi['pickup_datetime'].dt.month
taxi["day"] = taxi['pickup_datetime'].dt.day
taxi["hour"] = taxi['pickup_datetime'].dt.hour
taxi['weekday'] = taxi['pickup_datetime'].apply(week_num)
taxi['holiday'] = taxi['pickup_datetime'].apply(holiday)
taxi['work'] = taxi['pickup_datetime'].apply(lambda x:
                                            1 if x.weekday() < 5
                                            and x.hour >7
                                            and x.hour <21
                                            else 0 )

weather_event = ['20160110', '20160113', '20160117', '20160123', '20160205', '20160208', '20160215', '20160216',
                 '20160224', '20160225', '20160314', '20160315', '20160328', '20160329', '20160403', '20160404',
                 '20160530', '20160628']

weather_event = pd.Series(pd.to_datetime(weather_event, format = '%Y%m%d')).dt.date
weather_event = weather_event.astype('<U32')
weather_event = list(weather_event)

taxi["y-m-d"] = pd.to_datetime(taxi["pickup_datetime"]).apply(lambda x: x.strftime("%Y-%m-%d"))
taxi["extreme_weather"] = taxi["y-m-d"].apply(lambda x: 1 if x in weather_event else 0)
taxi["weather_event"] = taxi["extreme_weather"] # 날씨 (1:자연재해,  0:자연재해X)
taxi.drop(['y-m-d', 'extreme_weather'], axis=1, inplace=True)

taxi.to_csv("edited_test.csv", index = False)
