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



movieDictData = pd.read_csv("../data/revenueEditedreIDed.csv", index_col=False)
movieDictData.drop(movieDictData.columns[0], axis = 1, inplace = True)
movieDictData = movieDictData.drop(['adult','belongs_to_collection','homepage','imdb_id','original_language','original_title','overview','poster_path','production_companies','production_countries','spoken_languages','status','tagline','title','video'],axis=1)

print(movieDictData)

movieDict = {}

for index, row in movieDictData.iterrows():
    if len(movieDict.keys()) < 200:
        movieDict[row.id] = 0
    else:
        continue

print(movieDict)







movieData = pd.read_csv("../data/genresAppended-budgetFixed.csv", index_col=False)
movieData.drop(movieData.columns[0], axis = 1, inplace = True)


# # load data
dataset = movieData.values
# print(movieData)
# movieData = movieData[:50000]
# print(movieData)

hiTrainingSet = []
hiTestingSet = []
for index, row in movieData.iterrows():
    if row.movieId not in movieDict:
        if(len(hiTrainingSet) <= 10000):
            tempdf = pd.DataFrame(row).transpose()
            hiTrainingSet.append(tempdf)
    elif movieDict[row.movieId] < 10:
        tempdf = pd.DataFrame(row).transpose()
        hiTestingSet.append(tempdf)
        movieDict[row.movieId] += 1

    if(len(hiTrainingSet) == 10000 and len(hiTestingSet) == 2000):
        print(index)
        break


hiTrainingSetPD = pd.concat(hiTrainingSet)
print("Training Set: \n", hiTrainingSetPD)
hiTestingSetPD = pd.concat(hiTestingSet)
print("Testing Set: \n", hiTestingSetPD)

