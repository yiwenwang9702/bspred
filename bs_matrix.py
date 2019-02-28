import pandas as pd
import numpy as np
from .nbhd_p import *

def get_matrix(df):
    sigmoid = lambda x: 1 / (1 + np.exp(2*x-7.5))
    l = len(df)
    matrix = np.array([np.zeros(l) for i in range(l)])
    for i in range(l):
        matrix[i][i] = 1
        temporary = df.loc[i]
        c_i = [temporary['latitude'],temporary['longitude']]
        for j in range(i+1,l):
            temporary_1 = df.loc[j]
            c_j = [temporary_1['latitude'],temporary_1['longitude']]
            if abs(c_i[0]-c_j[0]) < 0.005 and abs(c_i[1]-c_j[1]) < 0.005:
                k = distance(c_i,c_j)/0.001

                if k < 5:
                    index = 0.5*sigmoid(k)
                    matrix[i][i] += index
                    matrix[j][j] += index
                    matrix[i][j]=index
                    matrix[j][i]=index
    return matrix



