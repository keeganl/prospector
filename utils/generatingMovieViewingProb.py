import numpy.matlib 
import numpy as np
import time
import datetime
import pandas as pd

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

# loop through and dot product the rows
for i in range(0, len(arr_i)):
    x = Weight("{}:{}".format(arr_u[i].id, arr_i[i].id), np.dot(arr_u[i].weights, arr_i[i].weights))
    dotProds.append(x)

with open('result.txt', 'w') as f:
    f.write("userId\tmovieId\t rating\n")
    for item in dotProds:
        f.write("{}\t{}\n".format(item.index, item.val))