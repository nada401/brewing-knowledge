import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter
from string import punctuation
import json
import sys
sys.path.append('../')
from helpers import *

def extract_keywords(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punkt_symbols = set(punctuation)
    removable_words= stop_words.union(punkt_symbols)

    filtered_tokens = [word for word in tokens if ((word not in removable_words) and word.isalpha())]

    # Stemming
    stemmer = SnowballStemmer('english')
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

    return stemmed_tokens

def exp_stem_extract(text, exp_stem_set):
    extracted_keywords = set(extract_keywords(text))
    return list(exp_stem_set.intersection(extracted_keywords))

def stem_df(x, exp_stem_set):
    x = x.copy()
    x.loc[:, 'text_lower'] = x['text'].str.lower()
    stems =  x['text_lower'].apply(lambda x: exp_stem_extract(x,exp_stem_set))
    x = x.drop(columns=['text', 'text_lower'])
    return pd.concat([x, stems], axis=1).rename(columns={'text_lower':'stems'})

def add_exp_stems(data_path):

    """
    Replace the text column with a list of the expert words present in that review and saves the result to a pickle file.

    Parameters:
    ----------
    data_path : str
        The path to the root directory containing the 'BeerAdvocate' and 'RateBeer' folders with review data.

    Notes:
    -----
    - This function reads review data from 'ratings_BA_clean.csv' in the 'BeerAdvocate' directory and
      'ratings_RB_clean.csv' in the 'RateBeer' directory.
    - It filters reviews marked as 'True' for 'review' status.
    - The function applies the `stems_df` function to add the stems to each review.
    - The processed DataFrame is saved as 'reviews_with_exp_stems.pkl' in the respective directory.
    """
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    reviews_ba = pd.read_csv(os.path.join(advocate_dir, 'ratings_BA_clean.csv'))
    rev_true_ba = reviews_ba[reviews_ba['review']==True]

    rb_dir = os.path.join(data_path, 'RateBeer')
    reviews_rb = pd.read_csv(os.path.join(rb_dir, 'ratings_RB_clean.csv'))
    rev_true_rb = reviews_rb[reviews_rb['review']==True]
    rev_true_rb = rev_true_rb[rev_true_rb['lang_tag']=='en']

    exp_stem_set = get_exp_stems_set(data_path)

    rev_true_ba = stem_df(rev_true_ba, exp_stem_set) 
    rev_true_ba.to_pickle(os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    rev_true_rb = stem_df(rev_true_rb, exp_stem_set)
    rev_true_rb.to_pickle(os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
