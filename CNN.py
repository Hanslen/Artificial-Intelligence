# Binary classifier is easier than classification into 10 categories.
# The first reason is to for binary problem, the output should be only true or false
# So, initially, the accuracy rate is 50%, while for 10 categories classification
# is 10%. Then, less category means we will have less output layer, so the model
# is not as complex as the 10 classification problem.

import numpy as np
import tensorflow as tf
from keras.datasets import cifar10
from keras import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras import optimizers

def load_cifar10():
    train, test = cifar10.load_data()
    xtrain, ytrain = train
    xtest, ytest = test
    ytrain_1hot = np.zeros((50000,10))
    ytest_1hot = np.zeros((10000,10))
    for i in range(0, 50000):
        ytrain_1hot[i][ytrain[i]] = 1
    for i in range(0, 10000):
        ytest_1hot[i][ytest[i]] = 1
    xtrain = xtrain/255
    xtest = xtest/255
    return xtrain, ytrain_1hot, xtest, ytest_1hot

# [1.4294919136047364, 0.49769999999999998]
def build_multilayer_nn():
    nn = Sequential()
    nn.add(Flatten(input_shape=(32, 32, 3)))
    hidden = Dense(units=100, activation="relu")
    nn.add(hidden) 
    output = Dense(units=10, activation="softmax")
    nn.add(output)
    return nn

def train_multilayer_nn(model, xtrain, ytrain):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy']) 
    model.fit(xtrain, ytrain_1hot, epochs=20, batch_size=32)       
 
# [0.7928062562942505, 0.72550000000000003]
def build_convolution_nn():
    nn = Sequential()
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same",input_shape=(32, 32, 3)))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    Dropout(0.25)
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(MaxPooling2D(pool_size=(4, 4)))
    Dropout(0.25)
    nn.add(Flatten(input_shape=(32, 32, 3)))
    nn.add(Dense(units=250, activation="relu"))
    nn.add(Dense(units=100, activation="relu"))
    nn.add(Dense(units=10, activation="softmax"))
    return nn
    
def train_convolution_nn(model, xtrain, ytrain):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy']) 
    model.fit(xtrain, ytrain_1hot, epochs=20, batch_size=32)  
    

def get_binary_cifar10():    
    train, test = cifar10.load_data()
    xtrain, ytrain = train
    xtest, ytest = test
    for i in range(0, 50000):
        if ytrain[i] == 0 or ytrain[i] == 1 or ytrain[i] == 8 or ytrain[i] == 9:
            ytrain[i] = 0
        else:
            ytrain[i] = 1
    for i in range(0, 10000):
        if ytest[i] == 0 or ytest[i] == 1 or ytest[i] == 8 or ytest[i] == 9:
            ytest[i] = 0
        else:
            ytest[i] = 1
    xtrain = xtrain/255
    xtest = xtest/255
    return xtrain, ytrain, xtest, ytest


# [0.16536357908844948, 0.93540000000000001]
def build_binary_classifier():    
    nn = Sequential()
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same",input_shape=(32, 32, 3)))
    nn.add(MaxPooling2D(pool_size=(2, 2)))
    Dropout(0.25)
    nn.add(Conv2D(32, (3, 3), activation='relu', padding="same"))
    nn.add(MaxPooling2D(pool_size=(4, 4)))
    Dropout(0.5)
    nn.add(Flatten(input_shape=(32, 32, 3)))
    nn.add(Dense(units=100, activation="relu"))
    nn.add(Dense(units=1, activation="sigmoid"))
    return nn

def train_binary_classifier(model, xtrain, ytrain):
    sgd = optimizers.SGD(lr=0.01)
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy']) 
    model.fit(xtrain, ytrain_1hot, epochs=30, batch_size=32)


if __name__ == "__main__":

    # Write any code for testing and evaluation in this main section.
    xtrain, ytrain_1hot, xtest, ytest_1hot = load_cifar10()
    nn1 = build_multilayer_nn()
    train_multilayer_nn(nn1, xtrain, ytrain_1hot)
    nn1.evaluate(xtest, ytest_1hot)

    nn2 = build_convolution_nn()
    train_convolution_nn(nn2, xtrain,ytrain_1hot)
    nn2.evaluate(xtest,ytest_1hot)

    xtrain, ytrain_1hot, xtest, ytest_1hot = get_binary_cifar10()
    nn3 = build_binary_classifier()
    train_binary_classifier(nn3,xtrain,ytrain_1hot)
    nn3.evaluate(xtest,ytest_1hot)

