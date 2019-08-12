from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from model import to_numpy



def SVM_model():
    model = SVC(kernel='linear', C=1e10)   # kernel='rbf' : kernal trick 사용
    return model



def model_fit(X_train, Y_train, X_val, Y_val, model):
    print(' >>> Train')
    model.fit(X_train, Y_train)

    Y_pre = model.predict(X_val)
    acc = accuracy_score(Y_val, Y_pre)

    print('\n >>> [ RESULT : SVM ]', end='\n\n')
    print('Accuracy: {:.5f}'.format(acc))



if __name__ == '__main__':
    X_train, Y_train, X_val, Y_val = to_numpy('./data/tmp/train.csv', './data/tmp/validation.csv')
    model = SVM_model()
    model_fit(X_train, Y_train, X_val, Y_val, model)