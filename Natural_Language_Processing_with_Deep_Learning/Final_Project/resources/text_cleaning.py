import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import string


def lemmatize_text(text):
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = WordNetLemmatizer()
    lem_text = []
    for w in w_tokenizer.tokenize(text):
        lem_text.append(lemmatizer.lemmatize(w))
        lem_text.append(" ")
    return ''.join(lem_text)
    # return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]  # apply on dataframe: df.text.apply(lemmatize_text)

# def lem_stem_text(text):
#     lemm_text = lemmatize_text(text)
#     lemm_stem_text = stem_text(lemm_text)
#     return lemm_stem_text


def clean_text(text):
    """ Takes Text and does the following
    1. Remove Stopwords - remove common stopwords in English
    2. Removing Numbers -- may want to revisit this if numbers are important (thinking like covid cases and such)
    3. Lemmatizes Text - revert word to its base form (ex. studies, studying to study)
     """
    no_punct = [char for char in text if char not in string.punctuation]
    no_numbers = "".join([i for i in no_punct if not i.isdigit()])
    lower_text = [word.lower() for word in no_numbers.split()
                  if word not in stopwords.words("english")]
    lower_text = ' '.join(lower_text)
    lemm_text = lemmatize_text(lower_text).strip()
    return lemm_text


df = pd.read_csv(
    '/Users/daphneyang/Desktop/5YMIDS_SP21/w266/266_final/nyt_data_collection/dataset/full_nyt_dataset.csv')
df
