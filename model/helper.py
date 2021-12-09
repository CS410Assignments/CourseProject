import pandas as pd
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")


def preprocess(text):
        # Clean text
        text = text.strip()  # Remove white space at the beginning and end
        text = text.replace('\n', ' ') # Replace the \n (new line) character with space
        text = text.replace('\r', '') # Replace the \r (carriage returns -if you're on windows) with null
        text = text.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space. 
        text = text.replace(' ', ' ') # Replace " " (a special character for space in HTML) with space.
        while '  ' in text:
            text = text.replace('  ', ' ') # Remove extra spaces
        
        # Parse document with SpaCy
        nlp_text = nlp(text)
        
        doc = [] # Temporary list to store individual document
    
        # Further cleaning and selection of text characteristics
        for token in nlp_text:
            if token.is_stop == False and token.is_punct == False and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ =="VERB"): # Retain words that are not a stop word nor punctuation, and only if a Noun, Adjective or Verb
                doc.append(token.lemma_.lower()) # Convert to lower case and retain the lemmatized version of the word (this is a string object)
        return doc
