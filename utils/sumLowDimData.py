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


movieDict = pd.read_csv("../data/revenueEditedreIDed.csv", index_col=False)
movieDict.drop(movieDict.columns[0], axis = 1, inplace = True)

print(movieDict)

movieRatingSums = {}

for index, row in movieDict.iterrows():
    movieRatingSums[row.id] = 0




movieData = pd.read_csv("../data/genresAppended-budgetFixed.csv", index_col=False)
movieData.drop(movieData.columns[0], axis = 1, inplace = True)


movieData = movieData
print(movieData)


for index, row in movieData.iterrows():
    movieRatingSums[row.movieId] += row.rating


print(movieRatingSums)




dataFrames = []
for index, row in movieDict.iterrows():
    tempdf = pd.DataFrame(row).transpose()
    tempdf['rating'] = movieRatingSums[row.id]
    dataFrames.append(tempdf)




resultAppended = pd.concat(dataFrames)
print(resultAppended)
resultAppended.to_csv("../data/lowDimData.csv")

