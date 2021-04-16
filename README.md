# prospector
Spring 2021 Database System Project

#### Team Name: 
The Prospectors
#### Keegan Lawley - `kwl17`
#### Braeden Warnick - `bmw16m`

### Dataset

https://www.kaggle.com/rounakbanik/the-movies-dataset

### Video

https://youtu.be/IU-i1TU6ba8


### Project Stage Reports
Stage 1: https://docs.google.com/document/d/1m9Min-U_t9d1X2JtwzepPQg_d0Q6kB_cKwT9SIDEyU0/edit

Stage 2: https://docs.google.com/document/d/1poouzxX12nrwGDZ2Uqo7PuKSwPUnGb6AZXKUeUWASC0/edit

Stage 3: https://docs.google.com/document/d/1Oyy4FspVV2HFQYYmbGOEJJsEBLrd48JHa6TgAp9dP74/edit

Stage 4: https://docs.google.com/document/d/1nVRdeflacWX3CssgmYCUWl6ccA4PxinxwICLX6XTzJ0/edit


### Code Files

#### Keegan: 

<strong>Vowpal Wabbit</strong>

This work was done using the Vowpal Wabbit cli tool 

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

To build a readable model, this requres the compilation of the tools within the library
```
awk -F "\"*,\"*\"*\"*" '{printf "%d |u %d |i %d\n", $3,$1,$2}' ./data/editedRatings.csv | 
  ./vowpal_wabbit/build/library/gd_mf_weights -I /dev/stdin --vwparams '-q ui --rank 10 --l2 0.001 --learning_rate 0.015 --passes 20 --decay_learning_rate 0.97 --power_t 0 -i movielens.reg --cache_file movielens.cache' 
```

<strong>Utility</strong>

`utils/generatingMovieViewingProb.py` This file computes the dot product of the feature weight vectors  for each movie and user that was the result of the readable Vowpal Wabbit model. 

`generateSparseMatrix.py` This file generates the model.csv which is the sparse matrix with metadata. It uses user and movie files from the matrix factorization because the ids were already listed there and they were easy to grab. It is almost 20GB but will generate in about 12 minutes. 

`utils/splitLogRegModel.py` The data ended up needing to be split into features and labels for sklearn so this file accomplishes that for the first logistic regression model while also storing the dataframes into csv so that this process does not need to occur every time.

`utils/log_reg_metrics.py` This file depends on the csvs generated from the above file to then train, test, and evaluate the logistic regression model.

`utils/nnls_ratings_metrics.py` This file depends on the csvs generated from the above file to then train, test, and evaluate the non-negative least squares regression model on user likelihood of seeing a movie.

To classify revenue per the paper I use this script `utils/revenueSeparator.py` this is built from the likelihood.csv that is generated from the `utils/generate_nnls_data.py` script

`utils/nnls_revenue_metrics.py` This file depends on the csvs generated from the above file to then train, test, and evaluate the non-negative least squares regression model on revenue movie.

#### Braeden:

Since the data was processed several times over the course of the semester, the data included in this repository for my section covers only the 3 data files used for running the main XGBoost models. The files needed for the Data Cleansing section can be found from our kaggle link and the rest are simply intermediary files used while working to get the data into proper form.

<strong>XGBoost Models</strong>

`xgBoost.py` This file contains the code that performs and tests the first binary logistic xgBoost model. Data file used `binaryXGBoostData.csv`

`highDim.py` This file contains the code that performs and tests the high dimensional second xgBoost model. Data file used `hiRevenueReclass.csv`

`lowDim.py` This file contains the code that performs and tests the low dimensional third xgBoost model. Data file used `loRevenueReclass.csv`

<strong>Data Cleansing</strong>

`dataCleanser.py` This file reads in the original movie metadata file and filters it by paper's original requirements.

`ratingsCleanser.py` This file reads in the original ratings file and filters out the movies that were removed by the previous files.

<strong>Major Utility</strong>

`resultsMetaCombine.py` This file reads in the results from the user x movie likelihoods and then builds a dataframe consisting of the likelihood data and the metadata for the associated movie.

`cleanGenres.py` This file reads in a file that contains a column of unrefined genres data, and cleans the column to consist of only an array of genre strings.

`appendingGenres.py` This file reads in a file that is result from `cleanGenres.py` and appends a column for each possible genre, marking the cell for the current movie a 1 or a 0 based on the existence of that column in the genre list for that movie. Both `cleanGenres.py` and `appendingGenres.py` are used for various files throughout the process of building the datasets for each model.

`revenueClassifier.py` This file reads in a file and reclassifies the revenue column to be one of nine results based on how it falls into the brackets introduced in the works surveyed.

`sumLowDimData.py` This file reads in the movie metadata and the likelihood results and aggregates the total movie-goer probability for each film.

`classifyBinaryBoost.py` This file simply classifies the likelihood for the first model into a binary format.

<strong>Minor Utility</strong>

`reID.py` This file reIDs the movies after the beginning filtering process was done.

`makeHiScreeningData.py` This file was written in the attempt at building the datasets to simulate small film screenings. This file led us to the conclusion our data was too insignificant in size to test that way.

`reformatModelforPandas.py` This file parses the likelihood results in a text file and builds a usable dataframe and csv from them for easier use later.

`middleLowDimClean.py` This file was used to help process data for the low dimensional model.

