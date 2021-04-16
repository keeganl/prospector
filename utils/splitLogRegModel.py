import pandas as pd
import datetime


def convertDate(d):
    return datetime.datetime.strptime(d, '%Y-%m-%d').timestamp()

def zeroify(x):
    if (x == -1):
        return 0
    else:
        return 1


df = pd.read_csv('../model.csv')
df = df.fillna('')
print(df)
df.drop(df.columns[[0]], axis = 1, inplace = True)
seenMovie = df.iloc[:,0]
seenMovie = seenMovie.apply(zeroify)
print(seenMovie)



metadata = df.drop(df.columns[[0]], axis = 1, inplace = False)
print(metadata.iloc[:,4])
metadata.iloc[:,4] = metadata.iloc[:,4].apply(convertDate)

seenMovie.to_csv('seenMovieCheck.csv')
metadata.to_csv('metadata.csv')
## end of csv generation