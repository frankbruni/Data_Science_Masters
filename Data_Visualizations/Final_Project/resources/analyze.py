import yake
import time
import pandas as pd
from pathlib import Path
import os
import regex as re
from tqdm.notebook import tqdm
tqdm.pandas()


# set directory to where this file is located
# folder_loc = os.path.dirname(os.path.realpath(__file__))
# os.chdir(Path(folder_loc))

# # from keyword_resources.stopwords import remove_stopw

# t0 = time.time()

kw_extractor = yake.KeywordExtractor()

# t1 = time.time()
# print('yake import   ' + str(t1-t0))

# # df = pd.read_excel('input/Theo Word Analysis (1).xlsx')
# df = pd.read_csv('/Users/daphneyang/Downloads/testing_data.csv')

# t2 = time.time()
# print('import   ' + str(t2-t1))

# col1 = 'answer'
# col1 = 'Describe how your business has been affected by the COVID 19 crisis'
# col2 = 'Which of the following industry types best describe your business?'
# col3 = 'What goods or services does your business provide to the neighborhood it is located in?'
# other_response = 'Other/None of the Above'

# cols = [col1, col2, col3]
# cols = ['answer']

# # fill na
# df[cols] = df[cols].fillna('')

# # create copy of original columns
# df_copy = df.copy()

# # stopwords
# for i in cols:
#     df[i] = df[i].apply(lambda x: remove_stopw(x))
#     df[i] = df[i].apply(lambda x: " ".join(x))

# t3 = time.time()
# print('stopwords ran   ' + str(t3-t2))

# find keywords


def word_in_list(word, keywords_list):
    matching_list = [s for s in keywords_list if word in s]
    # remove exact matches
    matching_list = [s for s in matching_list if len(word) != len(s)]
    return matching_list


def find_keywords(text_in):
    # parameters
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'jaro'
    windowSize = 1
    numOfKeywords = 150

    # yake extractor initialze with parameters
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                                dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)

    # extract keywords based on the parameters
    keywords_output = custom_kw_extractor.extract_keywords(text_in)
    # create dataframe of keywords output
    keywords_df = pd.DataFrame(keywords_output, columns=["word", "score"])
    del keywords_df['score']
    # make a list of just the words (exclude the scores)
    keywords = keywords_df['word'].to_list()
    # since every bi/trigram is going to include a unigram already....
    # lets just create the basis of our word search based on unigrams
    unigram_df = keywords_df[keywords_df['word'].apply(
        lambda x: len(x.split()) == 1)]
    # create column showing bi and trigrams that include the unigrams (for context)
    unigram_df['associated_phrases'] = unigram_df['word'].apply(
        word_in_list, args=(keywords,))

    return unigram_df


def search_for_words_around_word(word, text):
    # find the five words around the word before and after
    # sub = '(\w*)\W*(\w*)\W*(\w*)\W*(\w*)\W*(\w*)\W*(\w*)\W*(' + word + ')\W*(\w*)\W*(\w*)\W*(\w*)\W*(\w*)\W*(\w*)\W*(\w*)'
    # # find the first three instances of this word popping up
    # all_matches = re.findall(sub, text, re.I)
    # all_matches = [" ".join(x) for x in all_matches]
    # return all_matches

    # split into list of words
    text = text.split()
    # create an empty list to populate with our snippets of sentences
    pop_list = []
    # for each element that contains the word we're looking for
    for i in [a for a, x in enumerate(text) if x == word]:
        try:
            # try to get the six words before and after
            temp = text[i-6:i+6]
            # make the list a string
            temp = "..." + " ".join(temp) + "..."
            # append the snippet of text to the list
            pop_list.append(temp)
        except:
            # otherwise pass
            pop_list = ['']
    return pop_list


def find_instances(word, unaltered_string_list):
    # find where each instance of the word occured + six characters
    inilist = [m.start() for m in re.finditer(
        rf'\b{word}y?e?s?\b', unaltered_string_list)]
    if len(inilist) > 3:
        # cut the long long string of responses to the fourth time the word occurs
        unaltered_string_list = unaltered_string_list[:inilist[3] + 6]
        # now find three instances of the words around the keyword we're looking for
        list_instances = search_for_words_around_word(
            word, unaltered_string_list)
        return list_instances
    elif len(inilist) > 0:
        # cut the long long string of responses to the last time the word occurs + six characters
        unaltered_string_list = unaltered_string_list[:inilist[-1] + 6]
        # now find the instances of the words around the keyword we're looking for
        list_instances = search_for_words_around_word(
            word, unaltered_string_list)
        return list_instances
    else:
        return ''


# t4 = time.time()
# print('set functions   ' + str(t4-t3))


# # create long string of all responses for this question
# q1 = " ".join(df["answer"].to_list())
# # find the keywords and return a keywords dataframe
# q1_df = find_keywords(q1)

# t5 = time.time()
# print('ran keywords   ' + str(t5-t4))


# # find example instances of the word being used
# # use our unaltered dataframe
# q1_w_stopwords = " ".join(df_copy[col1].to_list())

# q1_df['context_fragments'] = q1_df['word'].progress_apply(find_instances, unaltered_string_list=q1_w_stopwords)

# t6 = time.time()
# print('ran fragments   ' + str(t6-t5))
