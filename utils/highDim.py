import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import xgboost

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from math import sqrt
from sklearn.metrics import mean_squared_error
from sklearn.metrics import log_loss

# userId	movieId	 rating


movieData = pd.read_csv("../data/hiRevenueReclass.csv", index_col=False, dtype={'revenue':int})
movieData.drop(movieData.columns[0], axis = 1, inplace = True)


# # load data
dataset = movieData.values
# print(movieData)
movieData = movieData[:10000]
# print(movieData)



X_cat = movieData.copy()
X_cat = movieData.select_dtypes(include=['int','float','object'])
X_enc = X_cat.copy()
#ONEHOT ENCODING BLOCK

# X_enc = pd.get_dummies(X_enc, columns=['userId','movieId','budget','revenue','popularity','runtime','release_date','vote_average','vote_count'],sparse=True)
X_enc = pd.get_dummies(X_enc, columns=['userId','movieId','budget','revenue','popularity','runtime','release_date','vote_average','vote_count'],sparse=True)
# # print(X_enc)
# movieData = movieData.drop(['userId','movieId','budget','revenue','popularity','runtime','release_date','vote_average','vote_count'],axis=1)
movieData = movieData.drop(['userId','movieId','budget','revenue','popularity','runtime','release_date','vote_average','vote_count'],axis=1)
# print(movieData)

FinalData = pd.concat([X_enc,movieData], axis=1)
# print(FinalData)




# trainy = FinalData['rating'].astype('int')
trainy = FinalData['rating'].astype('float')
trainy = trainy.loc[:,~trainy.columns.duplicated()]
trainx = FinalData.drop(['rating'], axis=1)
# test = FinalData.drop(['rating'], axis=1)
X_train,X_test, y_train,y_test = train_test_split(trainx, trainy, test_size=0.3)

clf = xgboost.XGBRegressor(max_delta_step = 0.05, learning_rate = 0.1,
# clf = xgboost.XGBRegressor(max_delta_step = 0.05, colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 200)




# print("y_train\n", y_train)
# print("y_test\n", y_test)
# print("X_train\n", X_train)
# print("X_test\n", X_test)

# print(clf)
clf.fit(X_train,y_train)
y_testpred= clf.predict(X_test)
dftestpred = pd.DataFrame(y_testpred)
# print("y_testpred:\n", dftestpred)
# y_pred = clf.predict(test)                     //unneccessary
# dfpred = pd.DataFrame(y_pred)                 //unneccessary
# print(dfpred)                                 //unneccessary


rms = sqrt(mean_squared_error(y_test, y_testpred))
print("RMSE :", rms)


# logLoss = log_loss(y_test, y_testpred, eps=1e-15, normalize=True, sample_weight=None, labels=None)
# print("LogLoss :", logLoss)



from sklearn.metrics import r2_score
r2score = r2_score(y_test, y_testpred)
print("R^2 Score: ", r2score)



from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

kfold = KFold(n_splits=10, random_state=7, shuffle=True)
# results = cross_val_score(clf, trainx, trainy, cv=kfold)                      // check this and next line to see important differences between trainx and X_train in this context
results = cross_val_score(clf, X_train, y_train, cv=kfold)                      
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))