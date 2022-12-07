# Data processing
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def load_data(credits_file,movies_file):
    # Read in data
    df1 = pd.read_csv('dataset/tmdb_5000_credits.csv')
    df2 = pd.read_csv('dataset/tmdb_5000_movies.csv')

    df1 = pd.read_csv(credits_file)
    df2 = pd.read_csv(movies_file)
    # print(df2.head(3)) # 20 columns
    df2 = df2.rename(columns={'id':'movie_id'})
    return df1,df2
# print(df2.head(3))

# print(f'df2 columns: {df2.columns}')

def movies_ranking(credits_file,movies_file):
    df1,df2 = load_data(credits_file,movies_file)
    df2=df2.merge(df1,on='movie_id') # 20 columns -> 23 columns
    columnNames = df2.columns
    # print(f'column names:{columnNames}')
    # print('df2 shape before ranking:',df2.shape) #(4803, 23)

    avg_vote = df2['vote_average'].mean()
    quantile_vote = df2['vote_count'].quantile(0.75)
    # print(f'mean of vote:{avg_vote}')
    # print(f'75% quantile of vote:{quantile_vote}')

    rank_movies=df2[df2['vote_count']>=quantile_vote]

    #shape of df2 dataframe after ranking
    # print('df2 shape after ranking:',rank_movies.shape) # (1203, 23)

    def score(x,q=quantile_vote,m=avg_vote):
        v=x['vote_count']
        R=x['vote_average']
        return (v/(v+q)*R)+(q/(v+q)*m)

    rank_movies['Score'] = rank_movies.apply(score,axis=1)

    # print(rank_movies[['original_title','Score']].sort_values('Score',ascending=False).head(10))
    pop = rank_movies.sort_values('Score',ascending=False)
    # print(pop.head(5))
    '''
        If you want to know the genres, you could use below command.
        In fact you could check all info based on keys stored in columnNames.
    '''
    # print(pop['genres'].iloc[0:5])
    return pop

if __name__ == '__main__':
    # print('Test')
    credits = 'dataset/tmdb_5000_credits.csv'
    movies = 'dataset/tmdb_5000_movies.csv'
    res = movies_ranking(credits,movies)
