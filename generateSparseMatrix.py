# Keegan Lawley

import numpy.matlib 
import numpy as np
import time
import datetime
import pandas as pd
import xlsxwriter
import json

totalUsers = 10000
totalMovies = 2614

class Item:
    def __init__(self, id, weights):
        self.id = id
        self.weights = weights

class Weight:
    def __init__(self, index, val):
        self.index = index
        self.val = val

class MovieMetadata:
    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata


def buildArray(filename):
    with open(filename) as reader:
        arr = []
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            s = line.split()
            x = np.array(s)
            # converts out of numpy array to list, just used to get the floats
            s = np.asfarray(x,float)
            # print(d, end='\n')
            d = Item(id=int(s[0]), weights=s[1:])
            arr.append(d)

            line = reader.readline()
    return np.squeeze(arr)


def getMetadata():
    revenueEdited = pd.read_csv("./utils/revenueEditedreIDed.csv")
    print("Revenue Movie dataset")
    
    obj = dict()
    arr = []
    for index, row in revenueEdited.iterrows():
        obj = {
            'title': row.title, 
            'budget': row.budget,
            'popularity': row.popularity, 
            'revenue': row.revenue,
            'runtime': row.runtime,
            'release_date': row.release_date,
            'vote_average': row.vote_average, 
            'vote_count': row.vote_count,
            'genres': []}
        m = MovieMetadata(row.id, obj)
        genreArr = []
        genreObj = row.genres.replace("'", '"')
        gHardcoded = {
            'Comedy': 0,
            'Drama': 0,
            'Romance': 0,
            'Adventure': 0,
            'Fantasy': 0,
            'Action': 0,
            'Mystery': 0,
            'Thriller': 0,
            'Science Fiction': 0,
            'Horror': 0,
            'Music': 0,
            'Family': 0,
            'Crime': 0,
            'Western': 0,
            'Animation': 0,
            'War': 0,
            'History': 0,
            'Documentary': 0
        }
        # once the number of genres is know just fix here
        for g in json.loads(genreObj):
            gHardcoded[g["name"]] = 1
        genreArr = list(gHardcoded.values())
        print(genreArr)
        obj['genres'] = genreArr
        # print( obj['genres'])
        arr.append(m)
    return arr


tStart = time.perf_counter()

arr_i = buildArray('i.quadratic') 
arr_u  = buildArray('u.quadratic') 
allMovieMetadata = getMetadata()

dotProds = []
watchedMovies = []

for i in range(0, 10000):
    x = Weight((arr_u[i].id, arr_i[i].id), np.dot(arr_u[i].weights, arr_i[i].weights))
    dotProds.append(x)
    watchedMovies.append((arr_u[i].id, arr_i[i].id))


# build -1/1 matrix (extremely sparse)
seenMovies = np.ones((totalUsers,totalMovies))
seenMovies = np.negative(seenMovies)
for watch in watchedMovies:
    # print(str(watch[0]) + "\t" + str(watch[1]))
    seenMovies[watch[0]-1][watch[1]-1] = 1
        
print(len(allMovieMetadata))

# assign metadata for logistic regression, this model is 30 GB!!
dfs = []
with open('data.vw', 'w') as f:
    for i in range(totalUsers):
        print("processing user: " + str(i) + " ...")
        for j in range(totalMovies):
            # print(i , j)
            # print("J", j)
            m = allMovieMetadata[j-1].metadata
            # print("M", m)

            data = [seenMovies[i][j], str(m['budget']),
            str(m['popularity']),
            str(m['revenue']),
            str(m['runtime']), 
            str(m['release_date']), 
            str(m['vote_average']), 
            str(m['vote_count'])] + m['genres']

            # dataStr = str(seenMovies[i][j]) + ' | ' + str(m['budget']) + ' ' + str(m['popularity']) + ' ' + str(m['revenue']) + ' ' + str(m['runtime']) + ' ' + str(m['release_date']) + ' ' + str(m['vote_average']) + ' ' + str(m['vote_count']) + ' ' + " ".join(m['genres']) + "\n"
            dfs.append(data)
            # f.write(dataStr)
df = pd.DataFrame(dfs)      
df.to_csv('model.csv')
# df.columns = ['seenMovie', 'budget', 'popularity', 'revenue', 'runtime', 'release_date', 'vote_average', 'vote_count', 'Comedy','Drama','Romance','Adventure','Fantasy','Action','Mystery','Thriller','Science Fiction','Horror','Music','Family','Crime','Western','Animation','War','History','Documentary']

# df = pd.DataFrame (seenMovies)
print(df)
# filepath = 'my_excel_file.xlsx'

# df.to_excel(filepath, index=False)

# uncomment if results.txt needs to be built
# with open('result.vw', 'w') as f:
#     f.write("userId\tmovieId\t rating\n")
#     for item in dotProds:
#         f.write("{}\t{}\n".format(item.index, item.val))

# workbook = xlsxwriter.Workbook('Expenses01.xlsx')
# worksheet = workbook.add_worksheet()


tEnd = time.perf_counter()
calcTime = tEnd - tStart
print("Proccessed in: ",  str(datetime.timedelta(seconds=calcTime))) 