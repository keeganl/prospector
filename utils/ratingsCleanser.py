import pandas as pd

revenueEdited = pd.read_csv("../data/revenueEdited.csv")
print("Edited Revenue Movie dataset")
print(revenueEdited)
print("\n")


ratingsdf = pd.read_csv("../data/ratings.csv")
print("Ratings dataset")
print(ratingsdf)

dataFrames = []
for index, row in ratingsdf.iterrows():
    tempID = row[1]
    if(not(revenueEdited.query("@tempID == id").empty)):
        tempdf = pd.DataFrame(row).transpose()
        dataFrames.append(tempdf)

ratingsEdited = pd.concat(dataFrames)
print(ratingsEdited)
ratingsEdited.to_csv("../data/editedRatings.csv")