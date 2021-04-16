# Keegan Lawley

import time
import datetime
import pandas as pd
import xlsxwriter
import json


class MovieMetadata:
    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata



def getMetadata():
    revenueEdited = pd.read_csv("./revenueEditedreIDed.csv")
    print("Revenue Movie dataset")
    
    objofObjs = dict()
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
        objofObjs[m.id] = m
    return objofObjs

tStart = time.perf_counter()

df = pd.read_csv('./movie-likelihood.txt', delimiter = "\t")
df.columns = ["userId", "movieId", "rating"]
# df = df.astype({"userId": int, "movieId": int, "rating": float})

allMovieMetadata = getMetadata()

# debugging
# for key, value in allMovieMetadata.items():
#     print (key, value)
dfs = []

for index, row in df.iterrows():
    m = allMovieMetadata[int(row['movieId'])].metadata
    # print(metadata.metadata.items())
    data = [row['rating'], str(m['budget']),
    str(m['popularity']),
    str(m['revenue']),
    str(m['runtime']), 
    str(m['release_date']), 
    str(m['vote_average']), 
    str(m['vote_count'])] + m['genres']
    dfs.append(data)

print(df)

finalDF = pd.DataFrame(dfs)      
finalDF.to_csv('likelihoodmodel.csv')

print(finalDF)


# for i in range(totalUsers):
#     print("processing user: " + str(i) + " ...")
#     for j in range(totalMovies):
#         # print(i , j)
#         # print("J", j)
#         m = allMovieMetadata[j-1].metadata
#         # print("M", m)

#         data = [seenMovies[i][j], str(m['budget']),
#         str(m['popularity']),
#         str(m['revenue']),
#         str(m['runtime']), 
#         str(m['release_date']), 
#         str(m['vote_average']), 
#         str(m['vote_count'])] + m['genres']

#         # dataStr = str(seenMovies[i][j]) + ' | ' + str(m['budget']) + ' ' + str(m['popularity']) + ' ' + str(m['revenue']) + ' ' + str(m['runtime']) + ' ' + str(m['release_date']) + ' ' + str(m['vote_average']) + ' ' + str(m['vote_count']) + ' ' + " ".join(m['genres']) + "\n"
#         dfs.append(data)
#         # f.write(dataStr)

tEnd = time.perf_counter()
calcTime = tEnd - tStart
print("Proccessed in: ",  str(datetime.timedelta(seconds=calcTime))) 