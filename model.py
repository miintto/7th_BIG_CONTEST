import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam
from dataframe import to_numpy
from evaluate import evaluate




def dnn_model(input_dim, output_dim):
    model = Sequential()
    model.add(Dense(units = 10, activation = 'relu', input_dim = input_dim))
    model.add(Dense(units = 10, activation = 'relu'))
    model.add(Dense(units = 10, activation = 'relu'))
    model.add(Dense(units = output_dim, activation = 'sigmoid'))
    print(model.summary())

    return model



def model_fit(X_train, Y_train, X_val, model):
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

    Y_pred = model.predict_classes(X_val)
    Y_prob = model.predict(X_val)

    return Y_pred, Y_prob



if __name__ == '__main__':
    train = pd.read_csv('./data/tmp/train.csv', encoding = 'utf-8')
    validation = pd.read_csv('./data/tmp/validation.csv', encoding = 'utf-8')

    X_train, Y_train = to_numpy(train) 
    X_val, Y_val = to_numpy(validation)
    model = dnn_model(X_train.shape[1], Y_train.shape[1])
    Y_pred, Y_prob = model_fit(X_train, Y_train, X_val, model)
    validation.loc[:, 'DLY'] = Y_pred
    validation.loc[:, 'DLY_RATE'] = Y_prob
    validation.to_csv('./result.csv', index=False)
    evaluate('./result.csv', Y_val)
    