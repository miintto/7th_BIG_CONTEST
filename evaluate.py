import pandas as pd
import numpy as np



def evaluate(file, Y_val):
    data = pd.read_csv(file, encoding = 'utf-8')
    Y_pred = data.DLY.values
    Y_prob = data.DLY_RATE.values

    Y_val = Y_val.reshape(-1)

    crosstab = pd.crosstab(Y_pred, Y_val)
    crosstab.columns.name = 'Actual'
    crosstab.index.name = 'Pred'
    RMSE = np.mean((Y_val - Y_prob)**2)
    acc = sum(Y_val==Y_pred)/len(Y_val)
    pre = sum(Y_val[Y_pred==1]==1)/sum(Y_pred==1)
    rec = sum(Y_pred[Y_val==1]==1)/sum(Y_val==1)

    print('\n >>> [ RESULT ]', end='\n\n')
    print(crosstab, end='\n\n')
    print(' >>> Accuracy  : {:.5f}'.format(acc))
    print(' >>> RMSE      : {:.8f}'.format(RMSE), end='\n\n')
    print(' >>> Precision : {:.5f}  (Y로 예측한 값 중 실제 Y의 비율)'.format(pre))
    print(' >>> Recall    : {:.5f}  (실제 Y 중 Y로 예측한 비율)'.format(rec))
