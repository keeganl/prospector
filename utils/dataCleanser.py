import pandas as pd


moviedf = pd.read_csv("../archive/movies_metadata.csv")

data = []
data.append(moviedf.iloc[0])
newdf = moviedf[0:0]

dataFrames = []
for index, row in moviedf.iterrows():
    if('US' in str(row[13]).split('}, {')[0]):
        tempdf = pd.DataFrame(row).transpose()
        dataFrames.append(tempdf)

countryEdited = pd.concat(dataFrames)
print("Original DataSet")
print(moviedf) 
print("\n")   
print("Dataset that's been edited to include only films where the main production country is US")
print(countryEdited)    
print("\n")   


dataFrames.clear()
for index, row in countryEdited.iterrows():
    if(int(row[2]) > 5000000 and (int(row[15]) >= 0.05 * int(row[[2]]))):
        tempdf = pd.DataFrame(row).transpose()
        dataFrames.append(tempdf)

budgetEdited = pd.concat(dataFrames)

print("Dataset that's been edited to include only films where the budget is greater than $5 million, and of those which ones had a revenue greater than 1/20th of their budget.")
print(budgetEdited)
print("\n")   


budgetEdited.to_csv("revenueEdited.csv")