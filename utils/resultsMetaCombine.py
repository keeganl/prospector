import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
# userId	movieId	 rating

df = pd.read_csv('../data/result1.txt', delimiter = "\t")
df.columns = ["userId", "movieId", "rating"]

movieData = pd.read_csv("../data/revenueEditedreIDed.csv")

movieMetaDataDict = {}
for index, row in movieData.iterrows():
    movieMetaDataDict[row.id] = [row.budget, row.revenue, row.popularity, row.runtime, row.release_date, row.vote_average, row.vote_count, row.genres]


dataFrames = []
for index, row in df.iterrows():
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
resultAppended.to_csv("../data/result.csv")


