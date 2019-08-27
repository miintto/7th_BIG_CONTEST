import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from process import to_numpy, split
from evaluate import evaluate



def xgb_model(n, eta):
    booster = XGBClassifier(booster='gbtree', silent=False, eta=eta, subsampling=0.5,
                                objective='binary:logistic', n_estimators=n)
    return booster



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv')
    validation = pd.read_csv('./data/tmp/validation.csv')

    train_1, train_2 = split(train)
    validation_1, validation_2 = split(validation)

    ### 결측치 없는것
    X_train, Y_train = to_numpy(train_1)
    X_val, Y_val_1 = to_numpy(validation_1)
    model = xgb_model(n=100, eta=0.3)
    model.fit(X_train, Y_train.reshape(-1), eval_set=[(X_train, Y_train.reshape(-1))], eval_metric='auc')
    validation_1.loc[:, 'DLY'] = model.predict(X_val)
    validation_1.loc[:, 'DLY_RATE'] = model.predict_proba(X_val)[:, 1]

    ### 결측치 잇는것
    X_train, Y_train = to_numpy(train_2)
    X_val, Y_val_2 = to_numpy(validation_2)
    model = xgb_model(n=100, eta=0.3)
    model.fit(X_train, Y_train.reshape(-1), eval_set=[(X_train, Y_train.reshape(-1))], eval_metric='auc')
    validation_2.loc[:, 'DLY'] = model.predict(X_val)
    validation_2.loc[:, 'DLY_RATE'] = model.predict_proba(X_val)[:, 1]

    validation = pd.concat([validation_1, validation_2], sort=False)
    Y_val = np.concatenate([Y_val_1, Y_val_2])
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val, message = 'XG BOOST')