from joblib import load
from flask import Flask, request
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from joblib import dump
from datetime import datetime
import pygeohash as pgh
import numpy as np

# PATH = "C:/ITC/Hackathon/Parker/geo_df.csv"  # local
PATH = 'geo_df.csv'  # server
TIMER = '/timer.pkl'
TIME = 'AvgTime'
POINT = 'point'


class Timing:
    def __init__(self):
        """
        Extracting averaged time to find parking
        """
        self.data_name = PATH
        self.df = self.load_data()
        self.all_geohash = np.array(self.df.iloc[:, [0]])
        # self.X, self.y = self.X_y_split()
        # self.d = self.single_pt_haversine(self.lat, self.lng)

    def load_data(self):
        """ loading the data to pandas DataFrame and prints shape"""
        df = pd.read_csv(self.data_name)
        print(f'Data shape: {df.shape}')
        return df

    def single_pt_haversine(self, lat, lng, degrees=True):
        """
        'Single-point' Haversine: Calculates the great circle distance
        between a point on Earth and the (0, 0) lat-long coordinate
        """
        r = 6371  # Earth's radius (km). Have r = 3956 if you want miles

        # Convert decimal degrees to radians
        if degrees:
            lat, lng = map(radians, [lat, lng])

        # 'Single-point' Haversine formula
        a = sin(lat / 2) ** 2 + cos(lat) * sin(lng / 2) ** 2
        d = 2 * r * asin(sqrt(a))

        return d

    def get_geohash(self, lat, lng, precision=7):
        """Transforming latitude longitude coordinates to geohash"""
        geohash = pgh.encode(lat, lng, precision)
        return geohash


    def get_avg_time_d(self, lat, lng):
        """
        Getting averaged time
        :param lat: latitude coordinate
        :param lng: longitude coordinate
        :param time: time of searching parking
        @return: average parking time. If unknown - return -1
        """
        d = round(self.single_pt_haversine(lat, lng))
        time = self.df[TIME][self.df[POINT] == d].values
        if time:
            return float(time[0])
        else:
            return -1

    def find_closest_geohash(self, geohash):
        """Finding the closest geohash to a given geohash
        return tuple of (closest geohash, distance to the closest geohash)"""
        # all_geohash = np.array(self.df.iloc[:, [0]])
        d = [pgh.geohash_approximate_distance(geohash, i[0]) for i in self.all_geohash]
        closest_geo = self.all_geohash[np.argmin(d)]
        return closest_geo[0], np.argmin(d)

    def get_avg_time_geohash(self, lat, lng, time=None):
        """
        Getting averaged time
        :param lat: latitude coordinate
        :param lng: longitude coordinate
        :param time: time of searching parking
        @return: average parking time. If unknown - return -1
        """
        geohash = pgh.encode(lat, lng, 7)
        print(geohash)
        time = self.df['AvgTimeToPark'][self.df['Geohash'] == geohash].values
        print(time)
        if time:
            return float(time[0])
        else:
            closest_geo = self.find_closest_geohash(geohash)
            if closest_geo[1] <= 10000:  # If point is close in less than 10 km
                time = self.df['AvgTimeToPark'][self.df['Geohash'] == str(closest_geo[0])].values
                return time[0]
            else:
                return -1

    def save_to_pickle(self, dir):
        dump(self.__class__, dir)


app = Flask('Get averaged time for parking')

# @app.route('/'):
# def print_enter_params():
#     return ('Use the ROUTE: /get_avg_time\nEnter parameters: "lat","lng","time" for latitude, longitude and time\n' \
#            'Returned: Averages time to find parking (minutes)')


@app.route('/get_avg_time')
def get_avg_time():
    """Predicts a single prediction"""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    time = request.args.get('time')
    avg_time = timing.get_avg_time_geohash(float(lat), float(lng), None)  # replace None with time when relevant

    return str(int(avg_time))


if __name__ == '__main__':
    # loading the model from Pickle file:
    # with open(PATH+TIMER, 'rb') as f:
    #     y = pickle.load(f)
    # timing = load(PATH + TIMER)
    timing = Timing()
    app.run(host="0.0.0.0", port=8080)  # remote server
    # app.run(host='127.0.0.1', port=5000)  # local server
