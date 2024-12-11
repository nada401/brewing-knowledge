import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from string import punctuation
import json

def get_exp_stems(expert_terms):
    expert_terms_stemmed = {}
    for category, terms in expert_terms.items():
        tokens = [word_tokenize(term.lower()) for term in terms]
    
        stemmer = SnowballStemmer('english')
        stemmed_tokens = [stemmer.stem(word[0]) for word in tokens]
        expert_terms_stemmed[category] =  stemmed_tokens
    
    return expert_terms_stemmed

def exp_term_score(text_tokens, expert_terms_stemmed):
    scores = {category: sum(1 for term in text_tokens if term in terms)
              for category, terms in expert_terms_stemmed.items()}
    scores["expertness_score"] = sum(scores.values())
    return scores

def score_df(df, expert_terms_stemmed):
    scores_df = df["stems"].map(exp_term_score(expert_terms_stemmed)).apply(pd.Series)
    
    # Drop intermediate column and merge results
    return pd.concat([df, scores_df], axis=1)


def add_exp_scores(data_path):

    """
    Adds experience-based scores to  review data and saves the result to  a pickle file.

    Parameters:
    ----------
    data_path : str
        The path to the root directory containing the 'BeerAdvocate' and 'RateBeer' folders with review data.

    Notes:
    -----
    - This function reads review data from 'reviews_with_exp_stems.pkl' in the 'BeerAdvocate' directory and
      'reviews_with_exp_stems.pkl' in the 'RateBeer' directory.
    - The function applies the `score_df` function to add the stems to each review.
    - The processed DataFrame is saved as 'reviews_w_scores.pkl' in the respective directory.
    """
    with open( os.path.join(data_path, 'expert_terms.json'), 'r') as f:
        expert_terms = json.load(f)

    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    stems_ba = pd.read_pickle(os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    rb_dir = os.path.join(data_path, 'RateBeer')
    stems_rb = pd.read_pickle(os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
    
    expert_terms_stemmed = get_exp_stems(expert_terms)


    df_ba = score_df(stems_ba, expert_terms_stemmed) 
    df_ba.to_pickle(os.path.join(advocate_dir, 'reviews_w_scores.pkl'))

    df_rb = score_df(stems_rb, expert_terms_stemmed)
    df_rb.to_pickle(os.path.join(rb_dir, 'reviews_w_scores.pkl'))
