import pandas as pd
import numpy as np
from sklearn.metrics import auc, roc_curve



def evaluate(file, Y_val, message=None):
    data = pd.read_csv(file, encoding = 'utf-8')
    Y_pred = data.DLY.values
    Y_prob = data.DLY_RATE.values

    Y_val = Y_val.reshape(-1)

    crosstab = pd.crosstab(Y_pred, Y_val)
    crosstab.columns.name = 'Actual'
    crosstab.index.name = 'Pred'

    acc = sum(Y_val==Y_pred)/len(Y_val)
    RMSE = np.mean((Y_val - Y_prob)**2)
    fpr, tpr, thresholds = roc_curve(Y_val, Y_prob)
    AUC = auc(fpr, tpr)
    pre = sum(Y_val[Y_pred==1]==1)/sum(Y_pred==1)
    rec = sum(Y_pred[Y_val==1]==1)/sum(Y_val==1)
    f1 = (2*pre*rec)/(pre+rec)

    print('______________________________')
    print('     RESULT  :  {}'.format(message))
    print('==============================')
    print(crosstab)
    print('______________________________', end='\n\n')
    print('  Accuracy   :  {:.5f}'.format(acc))
    print('  RMSE       :  {:.8f}'.format(RMSE))
    print('  AUC        :  {:.5f}'.format(AUC)  , end='\n\n')
    print('  Precision  :  {:.5f}  \t(Y로 예측한 값 중 실제 Y의 비율)'.format(pre))
    print('  Recall     :  {:.5f}  \t(실제 Y 중 Y로 예측한 비율)'.format(rec))
    print('  F1 score   :  {:.5f}'.format(f1))
    print('______________________________', end='\n\n\n')
