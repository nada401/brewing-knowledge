import os
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from string import punctuation
import sys
sys.path.append('../')
from helpers import *

STOP_WORDS = set(stopwords.words('english'))
PUNCTUATION = set(punctuation)
REMOVABLE_WORDS = STOP_WORDS.union(PUNCTUATION)
STEMMER = SnowballStemmer('english')

def extract_keywords(text):
    """
    Tokenizes text, removes stopwords and punctuation, stems the tokens, and returns processed words.
    """
    return [STEMMER.stem(word) for word in word_tokenize(text.lower()) 
            if word.isalpha() and word not in REMOVABLE_WORDS]

def exp_stem_extract(text, exp_stem_set):
    """
    Extracts keywords present in a given expert stem set.
    """
    return list(set(extract_keywords(text)).intersection(exp_stem_set))

def stem_df(df, exp_stem_set):
    """
    Processes the DataFrame by extracting stems and returns the updated DataFrame.
    """
    df['stems'] = df['text'].str.lower().apply(lambda x: exp_stem_extract(x, exp_stem_set))
    return df.drop(columns=['text'])

def process_and_save_reviews(reviews_df, exp_stem_set, output_path):
    """
    Processes reviews DataFrame to add expert stems and saves the result.
    """
    # Filter relevant rows
    reviews_df = reviews_df[(reviews_df['review'] == True) & (reviews_df['lang_tag'] == 'en')]
    processed_df = stem_df(reviews_df, exp_stem_set)
    processed_df.to_pickle(output_path)

def add_exp_stems(data_path):
    """
    Replaces the text column with a list of expert words (stems) in reviews, saves as pickle files.
    """
    # Load the expert stem set
    exp_stem_set = get_exp_stems_set(data_path)

    # Directories
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    rb_dir = os.path.join(data_path, 'RateBeer')

    # Process BeerAdvocate Reviews
    reviews_ba = pd.read_csv(os.path.join(advocate_dir, 'ratings_BA_clean.csv'))
    process_and_save_reviews(reviews_ba, exp_stem_set, os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    # Process RateBeer Reviews
    reviews_rb = pd.read_csv(os.path.join(rb_dir, 'ratings_RB_clean.csv'))
    process_and_save_reviews(reviews_rb, exp_stem_set, os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
