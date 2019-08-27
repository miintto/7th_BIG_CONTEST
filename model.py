import numpy as np
import pandas as pd
from keras.layers import Dense, Dropout, LeakyReLU
from keras.models import Sequential
from keras.optimizers import Adam
from keras.initializers import glorot_normal
from process import to_numpy, to_categirical, standardization, sampling, split
from evaluate import evaluate



def dnn_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(units = 10, kernel_initializer=glorot_normal(), input_dim = input_dim))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(rate=0.25))
    model.add(Dense(units = 10, kernel_initializer=glorot_normal()))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(rate=0.25))
    model.add(Dense(units = 10, kernel_initializer=glorot_normal()))
    model.add(LeakyReLU(alpha=0.1))
    model.add(Dropout(rate=0.25))
    model.add(Dense(units = output_dim, activation = 'sigmoid'))
    # print(model.summary())

    return model



def data_process(data):
    data = to_categirical(data, 'ARP', n=5)
    data = to_categirical(data, 'ODP', n=4)
    data = to_categirical(data, 'FLO', n=8)
    data = to_categirical(data, 'STT_hour', n=24)
    data.NUM_FLT = standardization(data.NUM_FLT)
    data.WSPD = standardization(data.WSPD)
    data.VIS = standardization(data.VIS)
    data.TMP = standardization(data.TMP)
    data.PA = standardization(data.PA)
    return data



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv', encoding = 'utf-8')
    validation = pd.read_csv('./data/tmp/validation.csv', encoding = 'utf-8')
    train = data_process(train)
    validation = data_process(validation)

    train_1, train_2 = split(train)
    validation_1, validation_2 = split(validation)

    ### 결측치 없는것
    X_train, Y_train = to_numpy(train_1)
    X_val, Y_val_1 = to_numpy(validation_1)
    X_train, Y_train = sampling(0.5, X_train, Y_train)
    model = dnn_model(X_train.shape[1], Y_train.shape[1])
    adam = Adam(lr=0.003, beta_1=0.9, beta_2=0.99)
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=10, batch_size=128, verbose=1, shuffle = True)
    validation_1.loc[:, 'DLY'] = model.predict_classes(X_val)
    validation_1.loc[:, 'DLY_RATE'] = model.predict(X_val)

    ### 결측치 잇는것
    X_train, Y_train = to_numpy(train_2)
    X_val, Y_val_2 = to_numpy(validation_2)
    X_train, Y_train = sampling(0.5, X_train, Y_train)
    model = dnn_model(X_train.shape[1], Y_train.shape[1])
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.99)
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, Y_train, epochs=10, batch_size=128, verbose=1, shuffle = True)
    validation_2.loc[:, 'DLY'] = model.predict_classes(X_val)
    validation_2.loc[:, 'DLY_RATE'] = model.predict(X_val)

    validation = pd.concat([validation_1, validation_2], sort=False)
    Y_val = np.concatenate([Y_val_1, Y_val_2])
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val, message='DEEP LEARNING')
