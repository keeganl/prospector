# prospector
Spring 2021 Database System Project

#### Team Name: 
The Prospectors
#### Keegan Lawley - `kwl17`
#### Braeden Warnick - `bmw16m`

### Dataset

https://www.kaggle.com/rounakbanik/the-movies-dataset


### Project Stage Reports
Stage 1: https://docs.google.com/document/d/1m9Min-U_t9d1X2JtwzepPQg_d0Q6kB_cKwT9SIDEyU0/edit

Stage 2: https://docs.google.com/document/d/1poouzxX12nrwGDZ2Uqo7PuKSwPUnGb6AZXKUeUWASC0/edit

Stage 3: https://docs.google.com/document/d/1Oyy4FspVV2HFQYYmbGOEJJsEBLrd48JHa6TgAp9dP74/edit

Stage 4: https://docs.google.com/document/d/1nVRdeflacWX3CssgmYCUWl6ccA4PxinxwICLX6XTzJ0/edit


## Getting Started
---

<i>This project uses Python 3.</i>

This is an implementation of the <strong>Improving Box Office Result Predictions for Movies Using Consumer-Centric Models</strong>

The dependencies for this project can be found in the `requirements.txt`

The data from kaggle should be placed into a data folder that is within the main folder of this project. This structure is required for files to run properly due to pathing within code.

To process this data, Braeden has made a series of cleanser script found in utils. The first script that should be run is dataCleanser.py, followed by ratingsCleanser which requires the edited result from the first script.


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

I ran again and got actual data instead of the nans.

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

To perform the logistic regression I (Keegan) needed to build a sparse matrix from the data and then attach the metadata as features to the model.

I used this snippet to build the sparse matrix: 
The watched movies are the user-movie tuple from the readable model 
```python
seenMovies = np.zeros((totalUsers,totalMovies))
for watch in watchedMovies:
    # print(str(watch[0]) + "\t" + str(watch[1]))
    seenMovies[watch[0]-1][watch[1]-1] = 1
```

Ran into an issue where we had to re-ID the movies after Braeden cleaned the data. So he went back and did that (code for doing so can be found in utils/reID.py) and sent me the the new files to redo the matrix factorization and rebuild the readable model

From here I get all the metadata for the movies, for genre I flattened the array to be the genre names. This increases the size of the matrix but seemed to be the best way to represent this feature. The I could just pass this to vowpal wabbit and it would get binary encoded through them by default. The code to do all of this work is in `userRatings.py`  


The vw file built for the logistic regression was huge, 30 GB!!

Vowpal command for logistic regression: 

`vw train.vw -f model.vw --loss_function logistic`

After running the regression this was the result: 

<img src="./images/result of logistic regression.png" />

At the time of submitting the report I started testing the model and that involves grabbing some metadata for movies that were not in the dataset and running them against the model.

<strong>Update - Braeden - 03/22/21</strong>

After cleaning the data, reIDing what was needed, and getting back the corrected readable model, I started to translate the results of the Matrix Factorization for use by XGBoost.

Due to some complexities discovered within XGBoost, a lot of processing has had to be done and some still has to be done before building the model.

Up until now I have edited the results I received from the readable model using resultsMetaCombine.py to add the necessary metadata for each rating given in the results.

After successfully appending the metadata, in order for the binary:logistic regression to be performed, I need to encode all columns before proceeding. This can be done somewhat easily with one hot encoding through Sci-kit but I ran into an issue with the lists of genres contained within the metadata for each film.

This led me to writing cleanGenres.py so that I could parse the complex arrays and simplify them for easier processing later. The resulting CSV from this script is then fed to another script I've written named appendingGenres.py which collects all possible genres, adds the necessary column for it to the dataframe and marks it 1 or 0 depending on its presence in the genre list for the current film. This results with a dataset that can use hot one encoding for the majority of the characteristics, such as userID and movieID, but it also contains the binary result columns for all genres for later encoding purposes. 

At this moment the binary:logistic regression model should be completed soon, but the delays with processing the data as well as understanding ambiguity within the paper regarding the work to be done and libraries has delayed me more than previously hoped.