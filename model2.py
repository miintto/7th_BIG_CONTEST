import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from dataframe import to_numpy
from evaluate import evaluate



def SVM_model():
    model = SVC(kernel='linear', C=1e10, probability=True)   # kernel='rbf' : kernal trick 사용
    return model



def model_fit(X_train, Y_train, X_val, Y_val, model):
    print(' >>> Train')
    Y_train = Y_train.reshape(-1)
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_val)
    Y_prob = model.predict_proba(X_val)[: ,1]

    return Y_pred, Y_prob



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv', encoding = 'utf-8')
    validation = pd.read_csv('./data/tmp/validation.csv', encoding = 'utf-8')

    X_train, Y_train = to_numpy(train) 
    X_val, Y_val = to_numpy(validation)
    model = SVM_model()
    Y_pred, Y_prob = model_fit(X_train, Y_train, X_val, Y_val, model)
    validation.loc[:, 'DLY'] = Y_pred
    validation.loc[:, 'DLY_RATE'] = Y_prob
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val)