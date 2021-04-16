import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import json
# userId	movieId	 rating

ratingData = pd.read_csv('../data/editedRatingsreIDed.csv')

ratingData= ratingData[:1000]
ratingData.drop(ratingData.columns[[0,1]], axis = 1, inplace = True)
ratingData.drop(['timestamp'], axis = 1, inplace = True)


movieData = pd.read_csv("../data/revenueEditedreIDed.csv")

movieMetaDataDict = {}
for index, row in movieData.iterrows():
    movieMetaDataDict[row.id] = [row.budget, row.revenue, row.popularity, row.runtime, row.release_date, row.vote_average, row.vote_count, row.genres]


dataFrames = []
for index, row in ratingData.iterrows():
    tempdf = pd.DataFrame(row).transpose()
    templist = movieMetaDataDict[row.movieId]
    tempdf['budget'] = templist[0]
    tempdf['revenue'] = templist[1]
    tempdf['popularity'] = templist[2]
    tempdf['runtime'] = templist[3]
    tempdf['release_date'] = templist[4]
    tempdf['vote_average'] = templist[5]
    tempdf['vote_count'] = templist[6]
    tempdf['genres'] = templist[7]
    dataFrames.append(tempdf)

resultAppended = pd.concat(dataFrames)
print(resultAppended)


genreFrames = []
for index, row in resultAppended.iterrows():
    editedGenres = json.loads(str(row.genres).replace("'","\""))
    genreList = []
    for obj in editedGenres:
        genreList.append(obj['name'])
    row.genres = genreList
    tempdf = pd.DataFrame(row).transpose()
    genreFrames.append(tempdf)

genresCleaned = pd.concat(genreFrames)
print(genresCleaned)

genresCleaned.to_csv("../data/posRateHiDim.csv")

