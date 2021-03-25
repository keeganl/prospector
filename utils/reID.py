import pandas as pd

revenueEdited = pd.read_csv("../data/revenueEdited.csv")
keywordsEdited = pd.read_csv("../data/editedKeywords.csv")
ratingsEdited = pd.read_csv("../data/editedRatings.csv")

indexIDPairs = {}
for index, row in revenueEdited.iterrows():
    indexIDPairs[row.id] = index

print(indexIDPairs)


dataFrames = []
for index, row in revenueEdited.iterrows():
    row.id = indexIDPairs[row.id]
    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)


revenueReIDed = pd.concat(dataFrames)
print(revenueReIDed)
revenueReIDed.to_csv("../data/revenueEditedreIDed.csv")

dataFrames.clear()

dataFrames = []
for index, row in keywordsEdited.iterrows():
    row.id = indexIDPairs[row.id]
    tempdf = pd.DataFrame(row).transpose()
    dataFrames.append(tempdf)


keywordsReIDed = pd.concat(dataFrames)
print(keywordsReIDed)
keywordsReIDed.to_csv("../data/editedKeywordsreIDed.csv")


# dataFrames.clear()

# dataFrames = []
# for index, row in ratingsEdited.iterrows():
#     row.movieId = indexIDPairs[row.movieId]
#     tempdf = pd.DataFrame(row).transpose()
#     dataFrames.append(tempdf)


# ratingsReIDed = pd.concat(dataFrames)
# print(ratingsReIDed)
# ratingsReIDed.to_csv("../data/editedRatingsreIDed.csv")