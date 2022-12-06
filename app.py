# import spacy
import gensim
import gensim.corpora as corpora
from gensim import models
import streamlit as st
# from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import os, glob
import pickle
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from streamlit import components

# Load "en_core_web_sm"
# nlp = spacy.load("en_core_web_sm")
parser = English()

# Functions
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

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

# HTML Start here
HTML = """<div style="overflow-x: auto; padding: 1rem">{}</div>"""

st.header('Topic Modeling for Course Transcripts', )
course_name = st.text_input('Input your course number here and press enter (from 1 to 11):')
BASE = 'data/'

text_data = []

path = BASE + course_name
for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
        print("NAMES", filename)
        txt = ""
        for line in f:
            txt += line + " "
        tokens = prepare_text_for_lda(txt)
        text_data.append(tokens)

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)

for topic in topics:
    st.write(topic)

vis = gensimvis.prepare(ldamodel, corpus, dictionary)
html_string = pyLDAvis.prepared_data_to_html(vis)
components.v1.html(html_string, width=1300, height=800)
