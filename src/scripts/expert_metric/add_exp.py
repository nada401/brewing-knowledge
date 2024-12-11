import pandas as pd
import os
import sys
sys.path.append('../')
from helpers import *

def score_df(df, expert_categories, expert_terms_stemmed):
    for criterion in expert_categories:
        df[criterion] = df['stems'].apply(lambda cell: len(list(set(cell) & set(expert_terms_stemmed[criterion]))))
    df['expertness_score'] = df[expert_categories].sum(axis=1)
    return df


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
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    stems_ba = pd.read_pickle(os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    rb_dir = os.path.join(data_path, 'RateBeer')
    stems_rb = pd.read_pickle(os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
    
    expert_terms_stemmed = get_exp_stems(data_path)


    df_ba = score_df(stems_ba, expert_terms_stemmed) 
    df_ba.to_pickle(os.path.join(advocate_dir, 'reviews_w_scores.pkl'))

    df_rb = score_df(stems_rb, expert_terms_stemmed)
    df_rb.to_pickle(os.path.join(rb_dir, 'reviews_w_scores.pkl'))
