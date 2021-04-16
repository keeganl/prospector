import numpy as np
import pandas as pd
import time
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from vowpalwabbit import pyvw
from vowpalwabbit.sklearn_vw import VWClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import datetime


def calculateMeanSquareError(known, pred):
    return mean_squared_log_error(known, pred)

tStart = time.perf_counter()

seenMovie = pd.read_csv("./seenMovieCheck.csv")
metadata = pd.read_csv("./metadata.csv")
print(seenMovie)
print(metadata)
seenMovie.drop(seenMovie.columns[[0]], axis = 1, inplace = True)
metadata.drop(metadata.columns[[0]], axis = 1, inplace = True)


print(seenMovie)
print(metadata)
print("Data loaded")
print(seenMovie.shape, '\t', metadata.shape)
seenMovie = seenMovie.astype('int')
# split train and test set
X_train, X_test, y_train, y_test = train_test_split(metadata, seenMovie, test_size=0.3, random_state=256)

# build VW logistic regression model
# LogLossVal:  0.013283467177640678
# Mean Square Error of the Log for the 1st model:  0.00018478019510039388
print('Train\n', y_train)
model = VWClassifier(loss_function='logistic')
model.fit(X_train, y_train)
# predict model
y_pred = model.predict_proba(X_test)
print(y_pred)
print("Training complete for model 1...")

print("starting LogLoss...")
# get log loss for linear regression model 
logLossVal = log_loss(y_test, y_pred, eps=1e-15, normalize=True, sample_weight=None, labels=None)
# r2_score_nnls = r2_score(y_test, y_pred)
# print("NNLS R2 score", r2_score_nnls)
# mse_1 = calculateMeanSquareError(y_test, y_pred)
# m1_recall = recall_score(y_test, y_pred, average='binary', zero_division=0)
# m1_precision = precision_score(y_test, y_pred, average='binary', zero_division=0)
# accuracy_m1 = accuracy_score(y_test, y_pred); 
# print("Model 1 Accuracy: ", accuracy_m1)
print("LogLoss Model 1: ", logLossVal)
# print("Mean Square Error of the Log for the 1st model: ", mse_1)
# print("Recall 1st model: ", m1_recall)
# print("Precision 1st model: ", m1_precision)






# evaluate model
kfold = KFold(n_splits=10, random_state=7, shuffle=True)
results = cross_val_score(model, X_train, y_train, cv=kfold)                      
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


tEnd = time.perf_counter()
calcTime = tEnd - tStart
print("Proccessed in: ",  str(datetime.timedelta(seconds=calcTime))) 