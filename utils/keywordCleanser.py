import pandas as pd

revenueEdited = pd.read_csv("revenueEdited.csv")
print("Edited Revenue Movie dataset")
print(revenueEdited)
print("\n")


keywordsdf = pd.read_csv("../archive/keywords.csv")
print("Ratings dataset")
print(keywordsdf)

dataFrames = []
for index, row in keywordsdf.iterrows():
    tempID = row[0]
    if(not(revenueEdited.query("@tempID == id").empty)):
        tempdf = pd.DataFrame(row).transpose()
        dataFrames.append(tempdf)

keywordsEdited = pd.concat(dataFrames)
print(keywordsEdited)
keywordsEdited.to_csv("editedKeywords.csv")