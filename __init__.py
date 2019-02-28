import pandas as pd
import numpy as np
import googlemaps
from sklearn.externals import joblib
from sklearn import base

import os
import sys

from .bs_matrix import *
from .nbhd_p import *
from .get_path import *
from .plot_new import *
name = 'bspred'
path = get_path()
stations = pd.read_csv(path+'stations.csv', sep = ',', engine='python')

class compound_estimator(base.BaseEstimator, base.RegressorMixin):
    
    def __init__(self, estimator_1, estimator_2, alpha=1):
        self.e1 = estimator_1
        self.e2 = estimator_2
        self.alpha = alpha
    
    def fit(self, X, y):
        self.e1.fit(X, y)
        self.residuals = y - self.alpha * self.e1.predict(X)
        self.e2.fit(X, self.residuals)
        return self
    
    def predict(self, X):
        base_of_prediction = self.alpha * self.e1.predict(X)
        additional = self.e2.predict(X)
        return base_of_prediction + additional
    
def val_and_geo(addresses, key=None):
    if not key:
        return None
    gmaps = googlemaps.Client(key=key)
    names = []
    lat = []
    lon = []
    end = ', New York, NY'
    for address in addresses:
        result = gmaps.geocode(address+end)
        if result[0]['address_components'][0]['long_name'] != 'New York':
            lat.append(result[0]['geometry']['location']['lat'])
            lon.append(result[0]['geometry']['location']['lng'])
            names.append(address)
    return names, lat, lon


def predict(addresses, key=None):
    if not key:
        return None
        
    names, lat, lon = val_and_geo(addresses, key)
    df_raw = pd.DataFrame(
        {
            'address': names, 'latitude': lat, 'longitude': lon
        }
    )
    df_raw = df_raw.dropna(how='any')
    if len(df_raw) == 0:
        return None
    nbhdp = get_profile(df_raw)
    model_ac = joblib.load(path+'models/ac.pkl')
    model_dc = joblib.load(path+'models/dc.pkl')
    ac = model_ac.predict(nbhdp)
    dc = model_dc.predict(nbhdp)
    df_raw['Characteristic_Arrivals'] = ac
    df_raw['Characteristic_Departures'] = dc
    return df_raw





