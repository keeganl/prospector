# prospector
Spring 2021 Database System Project

#### Team Name: 
The Prospectors
#### Keegan Lawley - `kwl17`
#### Braeden Warnick - `bmw16m`


### Project Stage Reports
Stage 1: https://docs.google.com/document/d/1m9Min-U_t9d1X2JtwzepPQg_d0Q6kB_cKwT9SIDEyU0/edit

Stage 2: https://docs.google.com/document/d/1poouzxX12nrwGDZ2Uqo7PuKSwPUnGb6AZXKUeUWASC0/edit

Stage 3: https://docs.google.com/document/d/1Oyy4FspVV2HFQYYmbGOEJJsEBLrd48JHa6TgAp9dP74/edit

Stage 4: https://docs.google.com/document/d/1nVRdeflacWX3CssgmYCUWl6ccA4PxinxwICLX6XTzJ0/edit


## Getting Started
---

<i>This project uses Python 3.</i>

This is an implementation of the <strong>Improving Box Office Result Predictions for Movies Using Consumer-Centric Models</strong>

The dependecies for this project can be found in the `requirements.txt`

The library requires the data to be in a VW format. More information can be found [here](https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Input-format).


To format the data into VW Format
```
awk -F "\"*,\"*\"*\"*" '{printf "%d |u %d |i %d\n", $3,$1,$2}' ./data/editedRatings.csv > ratings.vw
```

```bash
awk -F "\"*,\"*\"*\"*" '{printf "%d |u %d |i %d\n", $3,$1,$2}' ./data/editedRatings.csv | \
  ./vowpal_wabbit/build/vowpalwabbit/vw /dev/stdin -b 18 -q ui --rank 10 --l2 0.001 \
  --learning_rate 0.015 --passes 20 --decay_learning_rate 0.97 --power_t 0 \
  -f movielens.reg --cache_file movielens.cache
```

To build a readable model 
```
awk -F "\"*,\"*\"*\"*" '{printf "%d |u %d |i %d\n", $3,$1,$2}' ./data/editedRatings.csv | 
  ./vowpal_wabbit/build/library/gd_mf_weights -I /dev/stdin --vwparams '-q ui --rank 10 --l2 0.001 --learning_rate 0.015 --passes 20 --decay_learning_rate 0.97 --power_t 0 -i movielens.reg --cache_file movielens.cache' 
```

Had to build Vowpal Wabbit from source to use the above command.

Results of training first model on 2 million ratings

```
finished run
number of examples per pass = 2563921
passes used = 5
weighted example sum = 12819605.000000
weighted label sum = 29291019100.000000
average loss = 49664524.000000 h
best constant = 2284.861328
total feature number = 294850915
```

<strong>Update - Keegan - 02/23/21</strong>

I ran again and got acutal data instead of the nans.

This data is in the `.quadratic` `.linear` and constant files. 
This is a readble version of the movielens.reg

Also leaving out cache because it is to big for Github.

How to interpret the output: 

```
constant: a float for the global constant
i.linear: featureweight
i.quadratic: featurerank1 weightrank2 weight...rankK weight
u.linear: featureweight
u.quadratic: featurerank1 weightrank2 weight...rankK weight
```
<strong>Update - Keegan - 03/21/21</strong>

### Linear Regression 

To perform the linear regression I (Keegan) needed to build a sparse matrix from the data and then attach the metadata as features to the model.

I used this snippet to build the sparse matrix: 
The watched movies are the user-movie tuple from the readable model 
```python
seenMovies = np.zeros((totalUsers,totalMovies))
for watch in watchedMovies:
    # print(str(watch[0]) + "\t" + str(watch[1]))
    seenMovies[watch[0]-1][watch[1]-1] = 1
```

Ran into an issue where we had to re-ID the movies after Braeden cleaned the data. So he went back and did that and sent me the the new files to redo the matrix factorization and rebuild the readable model

From here I get all the metadata for the movies, for genre I flattened the array to be the genre names. This increases the size of the matrix but seemed to be the best way to represent this feature. The I could just pass this to vowpal wabbit and it would get binary encoded through them by default. The code to do all of this work is in `userRatings.py`  


The vw file built for the linear regression was huge 30 GB!!
After running the regression this was the result: 

<img src="./images/result of linear regression.png" />

At the time of submitting the report I started testing the model and that involves grabbing some metadata for movies that were not in the dataset and running them against the model. 