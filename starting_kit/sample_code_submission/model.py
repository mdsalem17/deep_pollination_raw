'''
Sample predictive model.
You must supply at least 4 methods:
- fit: trains the model.
- predict: uses the model to perform predictions.
- save: saves the model.
- load: reloads the model.
'''
import pickle
import numpy as np   # We recommend to use numpy arrays
from os.path import isfile
from sklearn.base import BaseEstimator
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D,  Dropout, Activation, BatchNormalization
from keras.utils.np_utils import to_categorical
import tensorflow as tf



class model (BaseEstimator):
    
    
    def __init__(self):
        '''
        This constructor is supposed to initialize data members.
        Use triple quotes for function documentation. 
        '''
        self.num_train_samples=0
        self.num_feat=1
        self.num_labels=1
        self.is_trained=False
        self.input_shape=(128,128,3)
        
        model_cnn = Sequential()
        model_cnn.add(Conv2D(64, 3, activation='relu', input_shape=self.input_shape))
        model_cnn.add(MaxPooling2D(2))
        
        model_cnn.add(Conv2D(128, 3, activation='relu'))
        model_cnn.add(MaxPooling2D(2))
        
        model_cnn.add(Conv2D(256, 3, activation='relu'))
        model_cnn.add(MaxPooling2D(2))
        
        model_cnn.add(Flatten())
        
        model_cnn.add(Dense(512, kernel_initializer='uniform'))
        model_cnn.add(BatchNormalization())
        model_cnn.add(Activation('relu'))
        model_cnn.add(Dense(5, kernel_initializer='uniform', activation='sigmoid'))
        model_cnn.compile(loss='categorical_crossentropy',optimizer='nadam', metrics=['accuracy'])
        self.model_cnn = model_cnn
        print("Model:", self.model_cnn)
    

    def fit(self, X, y):
        '''
        This function should train the model parameters.
        
        Args:
            X: Training data matrix of dim num_train_samples * num_feat.
            y: Training label matrix of dim num_train_samples * num_labels.
        Both inputs are numpy arrays.
        For classification, labels could be either numbers 0, 1, ... c-1 for c classe
        or one-hot encoded vector of zeros, with a 1 at the kth position for class k.
        The AutoML format support on-hot encoding, which also works for multi-labels problems.
        Use data_converter.convert_to_num() to convert to the category number format.
        For regression, labels are continuous values.
        '''
        self.num_train_samples = X.shape[0]
        if X.ndim>1: self.num_feat = X.shape[1]
        print("FIT: dim(X)= [{:d}, {:d}]".format(self.num_train_samples, self.num_feat))
        num_train_samples = y.shape[0]
        if y.ndim>1: self.num_labels = y.shape[1]
        print("FIT: dim(y)= [{:d}, {:d}]".format(num_train_samples, self.num_labels))
        if (self.num_train_samples != num_train_samples):
            print("ARRGH: number of samples in X and y do not match!")
            return
    
        #Everything is good lets fit the data   
        categorical_labels = to_categorical(y, num_classes=5)
        X = X.reshape(len(X), 128, 128, 3)
#         class_weight = {0: 0.13,
#                         1: 1.}
        self.model_cnn.fit(X/255., categorical_labels, epochs=10, validation_split=0.2,batch_size=100)
        
        self.is_trained=True
        print("FIT: Training Successful")

    def predict(self, X):
        '''
        This function should provide predictions of labels on (test) data.
        
        Make sure that the predicted values are in the correct format for the scoring
        metric. For example, binary classification problems often expect predictions
        in the form of a discriminant value (if the area under the ROC curve it the metric)
        rather that predictions of the class labels themselves. For multi-class or multi-labels
        problems, class probabilities are often expected if the metric is cross-entropy.
        Scikit-learn also has a function predict-proba, we do not require it.
        The function predict eventually can return probabilities.
        '''
        num_test_samples = X.shape[0]
        if X.ndim>1: num_feat = X.shape[1]
        print("PREDICT: dim(X)= [{:d}, {:d}]".format(num_test_samples, num_feat))
        if (self.num_feat != 0) and (self.num_feat != num_feat):
            print("ARRGH: number of features in X does not match training data!")
        print("PREDICT: dim(y)= [{:d}, {:d}]".format(num_test_samples, self.num_labels))
        
        #everything is good lets predict
        X = X.reshape(len(X),128,128,3)
        y = self.model_cnn.predict(X/255.)
        print("PREDICT: Prediction done")
              
        return np.argmax(y, axis=1)

    def save(self, path="./"):
        model_name = path+'_model.h5'
        self.model_cnn.save(model_name)
        print("Model Saved : " + model_name)
#         pickle.dump(self.model_cnn, open(path + '_model.pickle', "wb"))

    def load(self, path="./"):
        modelfile = path + '_model.h5'
        self.model_cnn = tf.keras.models.load_model(modelfile)
#         if isfile(modelfile):
#             with open(modelfile, 'rb') as f:
#                 self.model = pickle.load(f)
        print("Model reloaded from: " + modelfile)
        self.is_trained = True
        return self
