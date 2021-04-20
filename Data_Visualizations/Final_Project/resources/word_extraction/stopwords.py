from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join
stopset = set(stopwords.words('english'))

# =============================================================================
# get stopwords
# =============================================================================
# Get all stopwords and make a list
# 'stopwords_lists'
stop_folder_path = 'resources/word_extraction/stopwords_lists'
stopwords_files_names = [f for f in listdir(
    stop_folder_path) if isfile(join(stop_folder_path, f))]

# add ending / in case the folder path doesnt have it
if str(stop_folder_path)[-1] != '/':
    stop_folder_path = stop_folder_path + str('/')

# read in all the stop words
for i in stopwords_files_names:
    lines = open(stop_folder_path + i).read().splitlines()
    stopset = stopset.union(set(lines))

# remove dups
stopset = list(dict.fromkeys(stopset))


def remove_stopw(text):
    # list_w = [re.sub(r'[^\w\s]', '', x.lower()) for x in list_w if pd.notnull(x)]
    text = text.lower()
    list_w = text.split(' ')
    list_w = [x for x in list_w if len(x) > 1]
    words_list = [w for w in list_w if not w in stopset]
    return ' '.join(words_list)


def get_stopwords():
    return stopset
