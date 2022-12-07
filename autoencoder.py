import pandas as pd

# Read in data
df1 = pd.read_csv('dataset/tmdb_5000_credits.csv')
df2 = pd.read_csv('dataset/tmdb_5000_movies.csv')
# print(df2.head(3)) # 20 columns
df2 = df2.rename(columns={'id':'movie_id'})
# print(df2.head(3))

# print(f'df2 columns: {df2.columns}')

df2=df2.merge(df1,on='movie_id') # 20 columns -> 23 columns
columnNames = df2.columns
print(f'column names:{columnNames}')
print('df2 shape before ranking:',df2.shape) #(4803, 23)
# print(df2.head(3))
