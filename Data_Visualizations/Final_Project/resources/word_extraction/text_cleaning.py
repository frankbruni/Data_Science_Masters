import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pandas as pd

def lemmatize_text(text):
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lem_text = []
    for w in w_tokenizer.tokenize(text):
        lem_text.append(lemmatizer.lemmatize(w))
        lem_text.append(" ")
    return ''.join(lem_text)
    # return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]  # apply on dataframe: df.text.apply(lemmatize_text)

def stem_text(text):
    porter_stemmer = PorterStemmer()
    tokens = text.split()
    stem_text = []
    for token in tokens:
        stem_text.append(porter_stemmer.stem(token))
        stem_text.append(" ")
    return ''.join(stem_text)
    # stemmed_tokens = [porter_stemmer.stem(token) for token in tokens]
    # return stemmed_tokens    # # apply on dataframe: df.text.apply(stem_text)

def lem_stem_text(text):
    lemm_text = lemmatize_text(text)
    lemm_stem_text = stem_text(lemm_text)
    return lemm_stem_text