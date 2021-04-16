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


movieData = pd.read_csv("../data/lowDimGenresAppended1.csv", index_col=False)
movieData.drop(movieData.columns[0], axis = 1, inplace = True)


# # print(movieData)
movieData = movieData[:100000]
# print(movieData)


dataFrames = []
for index, row in movieData.iterrows():
    if row.revenue <= 1000000:
        row.revenue = 1
    elif 1000000 < row.revenue <= 10000000:
        row.revenue = 2
    elif 10000000 < row.revenue <= 20000000:
        row.revenue = 3
    elif 20000000 < row.revenue <= 40000000:
        row.revenue = 4
    elif 40000000 < row.revenue <= 65000000:
        row.revenue = 5
    elif 65000000 < row.revenue <= 100000000:
        row.revenue = 6
    elif 100000000 < row.revenue <= 150000000:
        row.revenue = 7
    elif 150000000 < row.revenue <= 200000000:
        row.revenue = 8
    elif 200000000 < row.revenue:
        row.revenue = 9
    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)




revenueClassified = pd.concat(dataFrames)
print(revenueClassified)
revenueClassified.to_csv("../data/loRevenueReclass.csv")