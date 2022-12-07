import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Read two datasets
credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
movies = movies.rename(columns={'id':'movie_id'})

# Get TF-IDF matrix
tf_idf = TfidfVectorizer(stop_words='english')
movies['overview'] = movies['overview'].fillna("")
overviews = movies['overview']
tf_idf_matrix = tf_idf.fit_transform(overviews)
tf_idf_matrix.shape

# Compute the first cosine similarity matrix
cosine_sim1 = linear_kernel(tf_idf_matrix, tf_idf_matrix)
# Build a reverse map of indices and movie titles
indices1 = pd.Series(movies.index, index=credits['title']).drop_duplicates()

# Keywords, casts, crews, genres
movies['keywords'] = movies['keywords'].apply(literal_eval)
movies['genres'] = movies['genres'].apply(literal_eval)
credits['crew'] = credits['crew'].apply(literal_eval)
credits['cast'] = credits['cast'].apply(literal_eval)

# Get the director's name from the crew feature. If director is not listed, return an empty string
def get_director(crews):
    for crew in crews:
        if crew['job'] == 'Director':
            return crew['name']
    return ""

credits['director'] = credits['crew'].apply(get_director)

# Returns the list top 3 elements if the length of the list is greater than 3
# If not, get the entire list
def get_top3(items):
    if isinstance(items, list):
        names = [item['name'] for item in items]
        # Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[0:3]
        return names
    # Return empty list in case of missing data
    return []

credits['cast'] = credits['cast'].apply(get_top3)
credits['crew'] = credits['crew'].apply(get_top3)
movies['keywords'] = movies['keywords'].apply(get_top3)
movies['genres'] = movies['genres'].apply(get_top3)

# Convert all strings to lower case and strip names of spaces
def clean_data(items):
    if isinstance(items, list):
        return [str.lower(item.replace(" ", "")) for item in items]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(items, str):
            return str.lower(items.replace(" ", ""))
        else:
            return ''

movies['keywords'] = movies['keywords'].apply(clean_data)
movies['genres'] = movies['genres'].apply(clean_data)
credits['crew'] = credits['crew'].apply(clean_data)
credits['cast'] = credits['cast'].apply(clean_data)

# Merge two datasets for later usage
movies = movies.merge(credits, on='movie_id')

# Create a metadata string for each movie with keywords, cast, director, and genres information
def create_metadata(movies):
    res = ''
    res += ' '.join(movies['keywords'])
    res += ' '.join(movies['cast'])
    # print(x['director'])
    res += ' ' + movies['director'] + ' '
    res += ' '.join(movies['genres'])
    return res

movies['soup'] = movies.apply(create_metadata, axis=1)

# Use count vector and create a count matrix
# In this case, TF-IDF does not make sense
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movies['soup'])

# Compute the second cosine similarity matrix
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
movies = movies.reset_index()
indices2 = pd.Series(movies.index, index=credits['title'])

# First version
# Use the overview to get recommendations
def get_recommendations_v1(title, cosine_sim=cosine_sim1):
    i = indices1[title]
    sim_scores = list(enumerate(cosine_sim[i]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [m[0] for m in sim_scores]
    return credits['title'].iloc[movie_indices]

# Second version
# Use keywords, genres, cast, and director to get recommendations
def get_recommendations_v2(title, cosine_sim=cosine_sim2):
    i = indices2[title]
    sim_scores = list(enumerate(cosine_sim[i]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [m[0] for m in sim_scores]
    return credits['title'].iloc[movie_indices]


def get_recommendations(title):
    res = []
    v1 = get_recommendations_v1(title)
    v2 = get_recommendations_v2(title)
    for index, value in v1.items():
        if [index, value] in res:
            continue
        else:
            res.append([index, value])
    for index, value in v2.items():
        if [index, value] in res:
            continue
        else:
            res.append([index, value])  
    return res


def print_result(rec_movies):
    for index, value in rec_movies:
        print("Index: " + str(index) + ", " + "Movie name: " + value)

if __name__ == "__main__":

    rec_movies = get_recommendations('The Dark Knight Rises')
    print_result(rec_movies)

