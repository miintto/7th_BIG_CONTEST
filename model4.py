import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from process import to_numpy, split, sampling
from evaluate import evaluate



def rf_model(n_estimators):
    model = RandomForestClassifier(n_estimators=n_estimators, oob_score=True)
    return model



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv')
    validation = pd.read_csv('./data/tmp/validation.csv')

    train_1, train_2 = split(train)
    validation_1, validation_2 = split(validation)

    ### 결측치 없는것
    X_train, Y_train = to_numpy(train_1)
    X_val, Y_val_1 = to_numpy(validation_1)
    X_train, Y_train = sampling(0.5, X_train, Y_train)
    model = rf_model(100)
    model.fit(X_train, Y_train.reshape(-1))
    validation_1.loc[:, 'DLY'] = model.predict(X_val)
    validation_1.loc[:, 'DLY_RATE'] = model.predict_proba(X_val)[:, 1]

    ### 결측치 잇는것
    X_train, Y_train = to_numpy(train_2)
    X_val, Y_val_2 = to_numpy(validation_2)
    X_train, Y_train = sampling(0.5, X_train, Y_train)
    model = rf_model(100)
    model.fit(X_train, Y_train.reshape(-1))
    validation_2.loc[:, 'DLY'] = model.predict(X_val)
    validation_2.loc[:, 'DLY_RATE'] = model.predict_proba(X_val)[:, 1]

    validation = pd.concat([validation_1, validation_2], sort=False)
    Y_val = np.concatenate([Y_val_1, Y_val_2])
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val, message='RANDOM FOREST')