from joblib import load
from flask import Flask, request
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from joblib import dump
from datetime import datetime

# PATH = "C:/ITC/Hackathon/Parker"
DATA_1 = '/data1.csv'
TIMER = '/timer.pkl'
TIME = 'AvgTime'
POINT = 'point'


class Timing:
    def __init__(self):
        """
        Extracting averaged time to find parking
        """
        self.path = None
        self.data_name = DATA_1
        self.df = self.load_data()
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

    def get_avg_time(self, lat, lng, time=None):
        """
        Getting averaged time
        :param lat: latitude coordinate
        :param lng: longitude coordinate
        :param time: time of searching parking
        """
        d = round(self.single_pt_haversine(lat, lng))
        time = self.df[TIME][self.df[POINT] == d].values[0]
        return float(time)

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
    avg_time = timing.get_avg_time(float(lat), float(lng), None)  # replace None with time when relevant

    return str(round(avg_time))


if __name__ == '__main__':
    # loading the model from Pickle file:
    # with open(PATH+TIMER, 'rb') as f:
    #     y = pickle.load(f)
    # timing = load(PATH + TIMER)
    timing = Timing()
    app.run(host="0.0.0.0", port=8080)
