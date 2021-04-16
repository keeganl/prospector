import numpy as np
import pandas as pd
import time
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from vowpalwabbit import pyvw
from vowpalwabbit.sklearn_vw import VWClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report

import datetime



def calculateMeanSquareError(known, pred):
    return mean_squared_log_error(known, pred)


tStart = time.perf_counter()

seenMovie = pd.read_csv("./seenMovieLikelihood.csv")
metadata = pd.read_csv("./metadataLikelihood.csv")
# print(seenMovie)
# print(metadata)
seenMovie.drop(seenMovie.columns[[0]], axis = 1, inplace = True)
metadata.drop(metadata.columns[[0]], axis = 1, inplace = True)

print(seenMovie)
print(metadata)
print("Data loaded")
print(seenMovie.shape, '\t', metadata.shape)
seenMovie = seenMovie.astype('int')
# split train and test set
X_train, X_test, y_train, y_test = train_test_split(metadata, seenMovie, test_size=0.3, random_state=1, shuffle=True, stratify = seenMovie)

# build model 2 nnls regression model
reg_nnls = LinearRegression(positive=True)
y_pred_nnls = reg_nnls.fit(X_train, y_train).predict(X_test)
r2_score_nnls = r2_score(y_test, y_pred_nnls)
print("NNLS R2 score", r2_score_nnls)
logLossVal_nnls = log_loss(y_test, y_pred_nnls, eps=1e-15, normalize=True, sample_weight=None, labels=None)

scaled_test = minmax_scale(y_test, feature_range=(0,1))
scaled_pred = minmax_scale(y_pred_nnls, feature_range=(0,1))
mse_2 = calculateMeanSquareError(scaled_test, scaled_pred)
# m2_recall = recall_score(y_test, y_pred_nnls, average='binary')
# m2_precision = precision_score(y_test, y_pred_nnls, average='binary')
print("LogLoss Model 2: ", logLossVal_nnls)
print("Mean Square Error of the Log for the 2nd model: ", mse_2)
# print("Recall 2nd model: ", m2_recall)
# print("Precision 2nd model: ", m2_precision)


# evaluate model
kfold = KFold(n_splits=10, random_state=7, shuffle=True)
results = cross_val_score(reg_nnls, X_train, y_train,  cv=kfold)                      
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

tEnd = time.perf_counter()
calcTime = tEnd - tStart
print("Proccessed in: ",  str(datetime.timedelta(seconds=calcTime))) 