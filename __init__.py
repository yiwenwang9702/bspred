#Please make sure that the input is a pandas dataframe containing information of the coordinates. The output will also be a dataframe.

import pandas as pd
import numpy as np
import os

from .bs_matrix import *
from .nbhd_p import *
from .pre_by_model import *

def predict(df_raw):
    df = df_raw[['latitude','longitude']]
    df = df.dropna(how='any')
    Nbhd_profile = get_profile(df)
    Arrivals, Departures= pre_simple(Nbhd_profile)
    if len(Arrivals)>1:
        matrix = get_matrix(df)
        inverse = np.linalg.inv(matrix)
        Departures_corrected = inverse.dot(Departures)
        Arrivals_corrected = inverse.dot(Arrivals)
        df['Arrivals'] = Arrivals_corrected
        df['Departures'] = Departures_corrected
    else:
        df['Arrivals'] = Arrivals
        df['Departures'] = Departures
    return df

#def predict_with_Citibike(df_raw, remove_list):

