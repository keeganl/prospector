import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import xgboost


# userId	movieId	 rating



movieData = pd.read_csv("../data/result1.csv", index_col=False)
movieData.drop(movieData.columns[[0,1]], axis = 1, inplace = True)




# # load data
dataset = movieData.values
# print(movieData)

movieGenres = {}
for x in movieData.genres:
    genreList = x.strip('][').split(', ')
    for y in genreList:
        if y not in movieGenres:
            movieGenres[y] = 1


print(movieGenres)

# count = 0
dataFrames = []
for index, row in movieData.iterrows():
    row.budget = int(row.budget)
    tempdf = pd.DataFrame(row).transpose()
    for x in movieGenres:
        if(x in row.genres):
            tempdf[x] = 1
        else:
            tempdf[x] = 0
    dataFrames.append(tempdf)
    # if count < 5:
    #     count += 1
    # else:
    #     break

genresAppended = pd.concat(dataFrames)
genresAppended.drop([''], axis = 1, inplace = True)
genresAppended.drop(['genres'], axis = 1, inplace = True)


print(genresAppended)
genresAppended.to_csv("../data/genresAppended.csv")