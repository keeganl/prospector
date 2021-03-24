import pandas as pd


class MovieMetadata:
    def __init__(self, id, metadata):
        self.id = id
        self.metadata = metadata

revenueEdited = pd.read_csv("revenueEditedreIDed.csv")
print("Revenue Movie dataset")

obj = dict()
allMovieMetadata = []
for index, row in revenueEdited.iterrows():
    obj = {'title': row.title, 'popularity': row.popularity, 'revenue': row.revenue, 'average_rating': row.vote_count}
    m = MovieMetadata(row.id, obj)
    allMovieMetadata.append(m)

for i in allMovieMetadata:
    print(i.metadata['title'])