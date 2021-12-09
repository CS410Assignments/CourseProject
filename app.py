import streamlit as st
import pandas as pd
import numpy as np
import spacy
import gensim
import gensim.corpora as corpora
from gensim import models
from model.helper import preprocess

nlp = spacy.load("en_core_web_sm")

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

st.header('Topic Modeling for Meeting Transcripts',)

lda_model = gensim.models.LdaModel.load('model/lda_model.model')
TFIDF = models.TfidfModel.load('model/tfidf_model.model')
ID2word = corpora.Dictionary.load('model/corpora_dict')

for index, topic in lda_model.print_topics(num_words=5):
    st.write('Topic {}: {}\n'.format(index+1,topic))

doc = st.text_input('Input your transcript here and press enter:')
doc_corpus = ID2word.doc2bow(preprocess(doc))
TFIDF_doc = TFIDF[doc_corpus]

for index, topic in lda_model.get_document_topics(TFIDF_doc):
    st.write('Topic {} Probability: {:.4f}\n'.format(index+1,topic))



