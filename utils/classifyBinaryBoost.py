import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import xgboost

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from math import sqrt
from sklearn.metrics import mean_squared_error


# userId	movieId	 rating

movieData = pd.read_csv("../data/genresAppended-budgetFixed.csv", index_col=False)
movieData.drop(movieData.columns[0], axis = 1, inplace = True)

movieData = movieData[:1000]
# print(movieData)

dataFrames = []
for index, row in movieData.iterrows():
    if(row.rating > 0):
        row.rating = 1
    else:
        row.rating = 0

    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)



FinalData = pd.concat(dataFrames)
print(FinalData)
FinalData.to_csv("../data/nonsparseBoost.csv")
