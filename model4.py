import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from dataframe import to_numpy
from evaluate import evaluate



def rf_model():
    model = RandomForestClassifier(n_estimators=100, oob_score=True)
    return model



def model_fit(X_train, Y_train, X_val, model):
    print(' >>> Train')
    Y_train = Y_train.reshape(-1)
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_val)
    Y_prob = model.predict_proba(X_val)[:, 1]
    print(' >>> Feature importances\n{}'.format(model.feature_importances_))

    return Y_pred, Y_prob



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv')
    validation = pd.read_csv('./data/tmp/validation.csv')

    X_train, Y_train = to_numpy(train) 
    X_val, Y_val = to_numpy(validation)
    model = rf_model()
    Y_pred, Y_prob = model_fit(X_train, Y_train, X_val, model)
    validation.loc[:, 'DLY'] = Y_pred
    validation.loc[:, 'DLY_RATE'] = Y_prob
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val)