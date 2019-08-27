import pandas as pd
from sklearn.ensemble import AdaBoostClassifier
from dataframe import to_numpy
from evaluate import evaluate
from model3 import tree_model



def boost_model(n_estimators, base_model):
    model = AdaBoostClassifier(n_estimators=n_estimators, base_estimator=base_model, learning_rate = 1)
    return model



def model_fit(X_train, Y_train, X_val, model):
    print(' >>> Train')
    Y_train = Y_train.reshape(-1)
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_val)
    Y_prob = model.predict_proba(X_val)[:, 1]

    return Y_pred, Y_prob



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv')
    validation = pd.read_csv('./data/tmp/validation.csv')

    train = train.loc[(train.AOD==0)&(train.ARP1==1), :]
    validation = validation.loc[(validation.AOD==0)&(train.ARP1==1), :]
    train = train.drop(['AOD', 'ARP1', 'ARP2', 'ARP3', 'ARP15', 'ARP_'], axis = 1)
    validation = validation.drop(['AOD', 'ARP1', 'ARP2', 'ARP3', 'ARP15', 'ARP_'], axis = 1)

    X_train, Y_train = to_numpy(train) 
    X_val, Y_val = to_numpy(validation)
    
    base_model = tree_model(12)
    model = boost_model(100, base_model)
    Y_pred, Y_prob = model_fit(X_train, Y_train, X_val, model)
    validation.loc[:, 'DLY'] = Y_pred
    validation.loc[:, 'DLY_RATE'] = Y_prob
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val)