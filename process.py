import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE



def standardization(data):
    mean = np.mean(data)
    sd = np.std(data)
    return (data - mean)/sd



def to_numpy(data):
    # data.loc[:, 'NUM_FLT'] = standardization(data.NUM_FLT)
    
    Y = data.loc[:, 'DLY']
    Y = Y.values.reshape(-1, 1)
    Y = (Y=='Y').astype(int)
    X = data.drop('DLY', axis=1).values
    
    return X, Y



def to_categirical(data, var, n=None):
    if n==None:
        n = max(data.loc[:, var])+1
    one_hot = np.eye(n)[data.loc[:, var].values].astype(int)

    for i in range(n):
        data.loc[:, var+str(i)] = one_hot[:, i]
    data = data.drop(var, axis=1)
    return data



def split(data):
    data1 = data.loc[~pd.isna(data.VIS)].copy()    
    data2 = data.loc[pd.isna(data.VIS)].copy()
    data2 = data2.drop(['WSPD', 'VIS', 'TMP', 'PA'], axis=1)

    return data1, data2



def sampling(ratio, X, Y):
    print(' >>> Sampling')
    sm = SMOTE(ratio=ratio, kind='regular')
    X_resampled, Y_resampled = sm.fit_sample(X, Y.reshape(-1))
    Y_resampled = Y_resampled.reshape(-1, 1)
    return X_resampled, Y_resampled
