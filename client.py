import pandas as pd
import numpy as np
import requests

URL = "http://ec2-3-70-178-147.eu-central-1.compute.amazonaws.com:8080"
ROUTE = "/get_avg_time"
SAMPLE_TEST = 20
LOCAL_URL = "http://127.0.0.1:5000"


def get_time_from_api(df, n=SAMPLE_TEST):
    """
    Predict from inference model, with data from DataFrame
    @:param df: pandas DataFrame with features to predict
    @:param n: int. number of rows to predict from. default 5.
    @:return: np.array of predictions ('0' or '1')
    """
    x = df.sample(n, random_state=42).to_dict('records')
    preds = np.array([float(requests.get(url=LOCAL_URL + ROUTE, params=row).text)
                      for row in x])
    return preds


if __name__ == '__main__':
    df = pd.read_csv("C:/ITC/Hackathon/Parker/rand_lat_lng_df.csv")
    times = get_time_from_api(df)
    print(times)
