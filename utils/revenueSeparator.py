import pandas as pd
import datetime


def convertDate(d):
    return datetime.datetime.strptime(d, '%Y-%m-%d').timestamp()

def zeroify(x):
    if (x == -1):
        return 0
    else:
        return 1

def classifyRevenue(x):
    if x <= 1000000:
        return 1
    elif 1000000 < x <= 10000000:
        return 2
    elif 10000000 < x <= 20000000:
        return 3
    elif 20000000 < x <= 40000000:
        return 4
    elif 40000000 < x <= 65000000:
        return 5
    elif 65000000 < x <= 100000000:
        return 6
    elif 100000000 < x <= 150000000:
        return 7
    elif 150000000 < x <= 200000000:
        return 8
    elif 200000000 < x:
        return 9

df = pd.read_csv('./likelihoodmodel.csv')
df.drop(df.columns[[0]], axis = 1, inplace = True)
print(df)

revenue = df.iloc[:,1]
revenue = revenue.apply(classifyRevenue)
print(revenue)

metadata = df.drop(df.columns[[1]], axis = 1, inplace = False)
metadata.iloc[:,4] = metadata.iloc[:,4].apply(convertDate)
print(metadata)

revenue.to_csv('revenue.csv')
metadata.to_csv('metadataForRevenue.csv')
# end of csv generation