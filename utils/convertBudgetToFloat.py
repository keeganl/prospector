import pandas as pd
import numpy as np
import json
from scipy.sparse import csr_matrix
import xgboost


# userId	movieId	 rating



movieData = pd.read_csv("../data/lowDimGenresAppended.csv", index_col=False)
movieData.drop(movieData.columns[0], axis = 1, inplace = True)






# count = 0
dataFrames = []
for index, row in movieData.iterrows():
    row.budget = float(str(row.budget))
    row.id = int(str(row.id))
    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)
    # if count < 5:
    #     count += 1
    # else:
    #     break


genresAppended = pd.concat(dataFrames)
print(genresAppended)
genresAppended.to_csv("../data/lowDimGenresAppended1.csv")