# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import nltk
nltk.download('genesis')
from nltk.collocations import *
from nltk import bigrams
from nltk.tokenize import word_tokenize
import pandas as pd
import string
from nltk.corpus import stopwords
import textblob  
from textblob import TextBlob
nltk.download('averaged_perceptron_tagger')
import numpy as np
import streamlit as st

# df_data = pd.read_csv("text_data.csv")

from pke.unsupervised import YAKE
from nltk.corpus import stopwords


########## DAPHNE ATTEMPT ######################
## creating document_list from data frame
def make_document_list(df, col_name):
    list_of_answers = df[col_name].tolist()
    document_list = " ".join(list_of_answers)
    return document_list

# #### trigram
def yake_trigram(document_list):
    collocation_list_trigram = []
    # 1. Create YAKE keyword extractor
    extractor = YAKE()

    # 2. Load document

    extractor.load_document(input=document_list,
                            language='en',
                            normalization=None)


    # 3. Generate candidate trigram keywords
    stoplist = stopwords.words('english')
    extractor.candidate_selection(n=3, stoplist=stoplist)

    # 4. Calculate scores for the candidate keywords
    extractor.candidate_weighting(window=3,
                                stoplist=stoplist,
                                use_stems=False)
    key_phrases = extractor.get_n_best(n=45, threshold=0.8)
    collocation_list_trigram.append(key_phrases)
    return collocation_list_trigram

# #### Bigram
def yake_bigram(document_list):
    collocation_list_bigram = []
    # 1. Create YAKE keyword extractor
    extractor = YAKE()

    # 2. Load document

    extractor.load_document(input=document_list,
                            language='en',
                            normalization=None)


    # 3. Generate candidate trigram keywords
    stoplist = stopwords.words('english')
    extractor.candidate_selection(n=2, stoplist=stoplist)

    # 4. Calculate scores for the candidate keywords
    extractor.candidate_weighting(window=2,
                                stoplist=stoplist,
                                use_stems=False)
    key_phrases = extractor.get_n_best(n=35, threshold=0.8)
    collocation_list_bigram.append(key_phrases)
    return collocation_list_bigram

# #### Unigram
def yake_unigram(document_list):
    collocation_list_unigram = []
    # 1. Create YAKE keyword extractor
    extractor = YAKE()

    # 2. Load document

    extractor.load_document(input=document_list,
                            language='en',
                            normalization=None)


    # 3. Generate candidate trigram keywords
    stoplist = stopwords.words('english')
    extractor.candidate_selection(n=1, stoplist=stoplist)

    # 4. Calculate scores for the candidate keywords
    extractor.candidate_weighting(window=1,
                                stoplist=stoplist,
                                use_stems=False)
    key_phrases = extractor.get_n_best(n=35, threshold=0.8)
    collocation_list_unigram.append(key_phrases)
    return collocation_list_unigram


# ##### Unigram list
def unigram_list(document_list):
    unigram_collocation = []
    collocation_list_unigram = yake_unigram(document_list)
    for each_list in collocation_list_unigram:
        new_collocation_list = []
        for each_collocation in each_list:
            new_collocation_list.append(each_collocation[0])
        unigram_collocation.append(new_collocation_list)
    return unigram_collocation

# ##### Bigram list
def bigram_list(document_list):
    bigram_collocation = []
    collocation_list_bigram = yake_bigram(document_list)
    for each_list in collocation_list_bigram:
        new_collocation_list = []
        for each_collocation in each_list:
            new_collocation_list.append(each_collocation[0])
        bigram_collocation.append(new_collocation_list)
    return bigram_collocation

# ##### Trigram list
def trigram_list(document_list):
    trigram_collocation = []
    collocation_list_trigram = yake_trigram(document_list)
    for each_list in collocation_list_trigram:
        new_collocation_list = []
        for each_collocation in each_list:
            new_collocation_list.append(each_collocation[0])
        trigram_collocation.append(new_collocation_list)
    return trigram_collocation, 

# #### Bigram & Unigram 

####only keep bigrams that don't have unigrams in it;final_bigram_list = []
def bi_uni_filter(document_list):
    bigram_collocation = bigram_list(document_list)
    unigram_collocation = unigram_list(document_list)
    final_bigram_list = []
    for i in range(len(bigram_collocation)):   
        final_bigram_list.append([bi for bi in bigram_collocation[i] if not any(uni in bi for uni in unigram_collocation[i])])
    return final_bigram_list

# #### Trigram & Bigram 

####only keep trigrams that don't have bigrams in it;
def tri_bi_filter(document_list):
    final_trigram_list = []
    trigram_collocation = trigram_list(document_list)
    bigram_collocation = bigram_list(document_list)
    for i in range(len(trigram_collocation)):   
        final_trigram_list.append([tri for tri in trigram_collocation[i] if not any(bi in tri for bi in bigram_collocation[i])])
    return final_trigram_list


## Put it all together
def get_keywords(df, col_name):
    document_list = make_document_list(df, col_name)
    final_bigram_list = bi_uni_filter(document_list)
    final_trigram_list = tri_bi_filter(document_list)
    final_unigram_list = unigram_list(document_list)
    final_list = final_unigram_list[0]
    if len(final_bigram_list[0]) > 0:
        final_list.extend(final_bigram_list[0])
    if len(final_trigram_list[0]) > 0:
        final_list.extend(final_trigram_list[0])
    return final_list