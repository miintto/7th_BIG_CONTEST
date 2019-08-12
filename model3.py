import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from model import to_numpy



def tree_model(n_depth):
    clf = DecisionTreeClassifier(criterion='entropy',max_depth=n_depth)
    return clf



def model_fit(X_train, Y_train, X_val, Y_val, clf):
    print(' >>> Train')
    clf.fit(X_train, Y_train)
    
    acc = clf.score(X_val, Y_val)
    RMSE = np.mean((Y_val -clf.predict_proba(X_val)[:, 1].reshape(-1, 1))**2)
    Y_pre = clf.predict(X_val).reshape(-1, 1)
    crosstab = pd.crosstab(Y_pre.reshape(-1), Y_val.reshape(-1))
    crosstab.columns.name = 'Actual'
    crosstab.index.name = 'Pred'
    pre = sum(Y_val[Y_pre==1]==1)/sum(Y_pre==1)[0]
    rec = sum(Y_pre[Y_val==1]==1)/sum(Y_val==1)[0]

    print('\n >>> [ RESULT : DECISION TREE ]', end='\n\n')
    print(crosstab, end='\n\n')
    print(' >>> Accuracy  : {:.5f}'.format(acc))
    print(' >>> RMSE      : {:.8f}'.format(RMSE), end='\n\n')
    print(' >>> Precision : {:.5f}  (Y로 예측한 값 중 실제 Y의 비율)'.format(pre))
    print(' >>> Recall    : {:.5f}  (실제 Y 중 Y로 예측한 비율)'.format(rec), end='\n\n')
    print(' >>> Feature importances : \n{}'.format(clf.feature_importances_))


if __name__ == '__main__':
    X_train, Y_train, X_val, Y_val = to_numpy('./data/tmp/train.csv', './data/tmp/validation.csv')
    clf = tree_model(10)
    model_fit(X_train, Y_train, X_val, Y_val, clf)