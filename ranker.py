import pandas as pd
from rank_bm25 import BM25Okapi
import csv
from gensim.parsing.preprocessing import remove_stopwords


#from query rank subreddits

def ranker(args) :
    if !(type(args) is str):
        num = args.num
        query = args.query
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
    return bm25.get_top_n(tokenized_query, rows, n=num)

def converter(q):
        #open csv file for wrting
        with open('test.csv','w', encoding = 'utf-8') as f:
            #acess each element in the returned list from bm25
            for i in range(0,len(q)):
                #write each subbreddit and submission to file
                f.write('%s %s\n' %((q)[i][0],(q)[i][1]))
        return
    
    
if __name__ =='__main__':
    #run ranker
    import argparse
    # Create the parser
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-n','--num',type=int,default=10)
    my_parser.add_argument('-q','--query',type=str,default="subreddit ranker")
    args = my_parser.parse_args()
    #convert bm25 list object to csv
    converter(ranker(args))