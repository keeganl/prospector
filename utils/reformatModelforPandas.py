with open('../data/result.txt', 'r') as file:
    data = file.readlines()

for x in range(0,len(data)):
    temp = data[x].split(":")
    user = temp[0]
    temp = temp[1].split("\t")
    movie = temp[0]
    weight = temp[1]
    data[x] = user + "\t" + movie + "\t" + weight

with open('../data/result1.txt', 'w') as file:
    file.writelines( data )