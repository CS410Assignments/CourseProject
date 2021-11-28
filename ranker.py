import pandas as pd
from rank_bm25 import BM25Okapi
import csv
from gensim.parsing.preprocessing import remove_stopwords


#from query rank subreddits
#
#Edit 'n=' in line 34 to change number of results
#Edit q in line 39 to change query
#Output is printed

def ranker(query) :
    #remove stopwords from query
    thisquery = remove_stopwords(query)
    #read csv file
    file = open('output-submissions.csv',encoding='utf-8')
    csvreader = csv.reader(file)
    #get header for csv (unused)
    header = []
    header = next(csvreader)
    #get rows of csv format: (subreddit,submissions)
    rows = []
    for row in csvreader :
        rows.append(row)
    file.close()
    #create and format corpus from submissions, remove stopwords from corpus
    corpus = []
    for i in rows:
        corpus.append(remove_stopwords(i[1]))
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    tokenized_query = thisquery.split(" ")
    #return ranked list with n number of documents with both subreddit and submissions
    return bm25.get_top_n(tokenized_query, rows, n=1)
    
    
if __name__ =='__main__':
    #run ranker
    q = "turkey"
    print(ranker(q))