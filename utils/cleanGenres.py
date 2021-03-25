import pandas as pd
import numpy as np
import json
# userId	movieId	 rating



movieData = pd.read_csv("../data/result.csv")

# print(movieData.head)

dataFrames = []
for index, row in movieData.iterrows():
    editedGenres = json.loads(str(row.genres).replace("'","\""))
    genreList = []
    for obj in editedGenres:
        genreList.append(obj['name'])
    row.genres = genreList
    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)


resultAppended = pd.concat(dataFrames)
print(resultAppended)
resultAppended.to_csv("../data/result1.csv")








# train_sparse_matrix = csr_matrix((df.rating.values, (df.userId.values,
#                                                df.movieId.values)))
# train_averages = dict()
# # get the global average of ratings in our train set.
# train_global_average = train_sparse_matrix.sum()/train_sparse_matrix.count_nonzero()
# train_averages['global'] = train_global_average
# print(train_averages)
# print(train_sparse_matrix)
# print(df)