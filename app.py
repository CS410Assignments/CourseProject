import spacy
import gensim
import gensim.corpora as corpora
from gensim import models
import streamlit as st

from spacy.lang.en import English
nlp = spacy.load("en_core_web_sm")

parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import wordnet as wn


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


from nltk.stem.wordnet import WordNetLemmatizer


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

import random
text_data = []
with open('data/4/01_examples-of-cyber-incidence.en.txt') as f:
    print("HERE")
    txt = ""
    for line in f:
        txt += line + " "
    print(txt)
    tokens = prepare_text_for_lda(txt)
    print(tokens)
    text_data.append(tokens)

with open('data/4/01_effects.en.txt') as f:
    print("HERE")
    txt = ""
    for line in f:
        txt += line + " "
    # print(txt)
    tokens = prepare_text_for_lda(txt)
    print(tokens)
    text_data.append(tokens)

with open('data/4/01_how-data-moves-application-layer.en.txt') as f:
    print("HERE")
    txt = ""
    for line in f:
        txt += line + " "
    # print(txt)
    tokens = prepare_text_for_lda(txt)
    print(tokens)
    text_data.append(tokens)

with open('data/4/01_weaponization.en.txt') as f:
    print("HERE")
    txt = ""
    for line in f:
        txt += line + " "
    # print(txt)
    tokens = prepare_text_for_lda(txt)
    print(tokens)
    text_data.append(tokens)

print("TXTDATA",text_data)
from gensim import corpora
dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]
import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

import gensim
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)
