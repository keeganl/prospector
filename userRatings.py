# Keegan Lawley

import numpy.matlib 
import numpy as np
import time
import datetime
import pandas as pd
import xlsxwriter

totalUsers = 99179
totalMovies = 2614

class Item:
    def __init__(self, id, weights):
        self.id = id
        self.weights = weights

class Weight:
    def __init__(self, index, val):
        self.index = index
        self.val = val

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

tStart = time.perf_counter()

arr_i = buildArray('i.quadratic') 
arr_u  = buildArray('u.quadratic') 

dotProds = []
watchedMovies = []

for i in range(0, len(arr_i)):
    x = Weight((arr_u[i].id, arr_i[i].id), np.dot(arr_u[i].weights, arr_i[i].weights))
    dotProds.append(x)
    watchedMovies.append((arr_u[i].id, arr_i[i].id))

seenMovies = np.zeros((totalUsers,totalMovies))
for watch in watchedMovies:
    print(str(watch[0]) + "\t" + str(watch[1]))
    seenMovies[watch[0]-1 ][watch[1]-1] = 1

df = pd.DataFrame (seenMovies)
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