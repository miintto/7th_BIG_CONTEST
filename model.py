import pandas as pd
import numpy as np
import datetime as dt
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam



def standardization(data):
    mean = np.mean(data)
    sd = np.std(data)
    return (data - mean)/sd



def to_numpy(train_data, val_data):
    print(' >>> Load data')
    train = pd.read_csv(train_data, encoding = 'utf-8')
    validation = pd.read_csv(val_data, encoding = 'utf-8')

    train.loc[:, 'NUM_FLT'] = standardization(train.NUM_FLT)
    validation.loc[:, 'NUM_FLT'] = standardization(train.NUM_FLT)
    
    Y_train = train.loc[:, 'DLY']
    Y_train = Y_train.values.reshape(-1, 1)
    Y_train = (Y_train=='Y').astype(int)
    X_train = train.drop('DLY', axis=1).values
    Y_val = validation.loc[:, 'DLY']
    Y_val = Y_val.values.reshape(-1, 1)
    Y_val = (Y_val=='Y').astype(int)
    X_val = validation.drop('DLY', axis=1).values

    return X_train, Y_train, X_val, Y_val



def dnn_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(units = 10, activation = 'relu', input_dim = input_dim))
    model.add(Dense(units = 10, activation = 'relu'))
    model.add(Dense(units = 10, activation = 'relu'))
    model.add(Dense(units = output_dim, activation = 'sigmoid'))
    print(model.summary())

    return model



def train(X_train, Y_train, X_val, Y_val, model):
    lr = 0.01
    batch_size = 256
    epochs = 5
    print(' >>> MODEL PARAMETERS')
    print(' >>> input_dim     : '+str(X_train.shape[1]))
    print(' >>> output_dim    : '+str(Y_train.shape[1]))
    print(' >>> learning rate : '+str(lr))
    print(' >>> batch_size    : '+str(batch_size))
    print(' >>> epochs        : '+str(epochs), end='\n\n')

    adam = Adam(lr=lr, beta_1=0.99, beta_2=0.9)
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose=1, shuffle = True)

    loss, acc = model.evaluate(X_val, Y_val)
    RMSE = np.mean((Y_val - model.predict(X_val))**2)
    Y_pre = model.predict_classes(X_val)
    crosstab = pd.crosstab(Y_pre.reshape(-1), Y_val.reshape(-1))
    crosstab.columns.name = 'Actual'
    crosstab.index.name = 'Pred'
    pre = sum(Y_val[Y_pre==1]==1)/sum(Y_pre==1)[0]
    rec = sum(Y_pre[Y_val==1]==1)/sum(Y_val==1)[0]

    print('\n >>> [ RESULT : DEEP LEARNING ]', end='\n\n')
    print(crosstab, end='\n\n')
    print(' >>> Loss      : {:.8f}'.format(loss))
    print(' >>> Accuracy  : {:.5f}'.format(acc))
    print(' >>> RMSE      : {:.8f}'.format(RMSE), end='\n\n')
    print(' >>> Precision : {:.5f}  (Y로 예측한 값 중 실제 Y의 비율)'.format(pre))
    print(' >>> Recall    : {:.5f}  (실제 Y 중 Y로 예측한 비율)'.format(rec))



if __name__ == '__main__':
    X_train, Y_train, X_val, Y_val = to_numpy('./data/tmp/train.csv', './data/tmp/validation.csv')
    model = dnn_model(X_train.shape[1], Y_train.shape[1])
    train(X_train, Y_train, X_val, Y_val, model)