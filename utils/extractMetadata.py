import pandas as pd
import json


class MovieMetadata:
    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata

revenueEdited = pd.read_csv("revenueEditedreIDed.csv")
print("Revenue Movie dataset")

obj = dict()
allMovieMetadata = []
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
    for g in json.loads(genreObj):
        genreArr.append(g["name"])
    obj['genres'] = genreArr
    print( obj['genres'])
    allMovieMetadata.append(m)

# for i in allMovieMetadata:
#     print(i.metadata['title'])