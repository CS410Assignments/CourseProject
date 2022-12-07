import numpy as np
import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate, GridSearchCV, train_test_split

# Read in data
df1 = pd.read_csv('dataset/tmdb_5000_credits.csv')
df2 = pd.read_csv('dataset/tmdb_5000_movies.csv')
# print(df2.head(3)) # 20 columns
df2 = df2.rename(columns={'id':'movie_id'})
df2=df2.merge(df1,on='movie_id') # 20 columns -> 23 columns
df2['user_id'] = np.random.randint(1, 100, df2.shape[0]) # 100 random user id for rating
columnNames = df2.columns

reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(df2[["user_id", "movie_id", "vote_average"]], reader)

algo = SVD(n_epochs = 10)
results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=10, verbose=True)

print("Average MAE: ", np.average(results["test_mae"]))
print("Average RMSE: ", np.average(results["test_rmse"]))

# Grid-Search for best params
param_grid = {
  'n_factors': [20, 50, 100],
  'n_epochs': [5, 10, 20]
}

gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=10)
gs.fit(data)

print(gs.best_score['rmse'])
print(gs.best_params['rmse'])

# best hyperparameters
best_factor = gs.best_params['rmse']['n_factors']
best_epoch = gs.best_params['rmse']['n_epochs']

# sample random trainset and testset
# test set is made of 20% of the ratings.
trainset, testset = train_test_split(data, test_size=.20)

# We'll use the famous SVD algorithm.
svd = SVD(n_factors=best_factor, n_epochs=best_epoch)

# Train the algorithm on the trainset
svd.fit(trainset)

def generate_recommendation(model, user_id, df, n_items):
   # Get a list of all movie IDs from dataset
   movie_ids = df["movie_id"].unique()

   # Get a list of all movie IDs that have been watched by user
   movie_ids_user = df.loc[df["user_id"] == user_id, "movie_id"]
    # Get a list off all movie IDS that that have not been watched by user
   movie_ids_to_pred = np.setdiff1d(movie_ids, movie_ids_user)

   # Apply a rating of 4 to all interactions (only to match the Surprise dataset format)
   test_set = [[user_id, movie_id, 4] for movie_id in movie_ids_to_pred]

   # Predict the ratings and generate recommendations
   predictions = model.test(test_set)
   pred_ratings = np.array([pred.est for pred in predictions])
   print("Top {0} item recommendations for user {1}:".format(n_items, user_id))
   # Rank top-n movies based on the predicted ratings
   index_max = (-pred_ratings).argsort()[:n_items]
   for i in index_max:
       movie_id = movie_ids_to_pred[i]
       print(df[df["movie_id"]==movie_id]["original_title"].values[0], pred_ratings[i])


# define which user ID that we want to give recommendation
userID = 23
# define how many top-n movies that we want to recommend
n_items = 10
# generate recommendation using the model that we have trained
generate_recommendation(svd, userID, df2, n_items)
