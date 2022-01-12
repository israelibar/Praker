import pandas as pd
import numpy as np
import pickle
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


PATH = "ec2-3-70-178-147.eu-central-1.compute.amazonaws.com"
DATA_1 = 'data1.csv'
TIMER = '/timer.pkl'
TIME = 'AvgTime'
POINT = 'point'


# SAVE_PATH = "C:/ITC/Flask/"
# MODEL_PICKLE_NAME = "churn_model.pkl"
# X_TEST_CSV_NAME = "X_test.csv"
# Y_PRED_CSV_NAME = "preds.csv"
# FEATURES = ['is_male', 'num_inters', 'late_on_payment',	'age',	'years_in_contract']
#
# SERVER_URL = "http://127.0.0.1:5000"
# ROUTE = "/predict_churn"

class Timing:
    def __init__(self):
        """
        Extracting averaged time to find parking
        """
        self.path = PATH
        self.data_name = DATA_1
        self.df = self.load_data()
        # self.X, self.y = self.X_y_split()
        # self.d = self.single_pt_haversine(self.lat, self.lng)

    def load_data(self):
        """ loading the data to pandas DataFrame and prints shape"""
        df = pd.read_csv(self.path + self.data_name)
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



if __name__ == '__main__':
    timing = Timing()
    timing.save_to_pickle(PATH + TIMER)
