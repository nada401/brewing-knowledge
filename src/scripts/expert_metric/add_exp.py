import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from string import punctuation

expert_terms = {
    "flavor": ['caramel', 'toffee', 'bready', 'biscuity', 'nutty', 'roasted', 'chocolate', 'coffee', 'mocha','molasses','syrupy','smokey','toasted','vanilla','cocoa','brown sugar',
              'hoppy', 'citrusy', 'tropical', 'floral', 'piney', 'resinous', 'herbal', 'grassy', 'earthy', 'dank', 'spicy', 'peppery', 'juicy', 'zesty', 'tangy', 'sharp', 'resin', 'bitterness',
               'estery',' fruity', 'berry',' cherry',' apple',' banana', 'pear', 'stone fruit', 'plum', 'fig', 'raisin', 'peach',' apricot', 'dark fruit', 'citrus zest', 'lemon', 'orange peel', 'pineapple', 'mango', 'lychee',
               'oaky', 'woody', 'bourbon', 'whiskey', 'rye', 'tequila', 'brandy','vinous', 'sour', 'tart', 'acidic', 'lacto', 'brett', 'farmhouse', 'honeyed', 'clove', 'bubblegum', 'funky', 'barnyard'], 
    "aroma": ['bouquet', 'nose', 'aromatic', 'fragrant','perfumed', 'faint', 'musky', 'dank', 'subtle', 'fruity', 'floral', 'yeasty', 'clean', 'malty', 'crisp', 'pungent', 'spicy', 'smokey', 'earthy'],  
    "mouthfeel": [ 'body','full-bodied', 'medium-bodied', 'light-bodied', 'thick', 'thin', 'mouthfeel', 'creamy', 'smooth', 'velvety', 'oily', 'astringent','tannic', 'chalky', 'drying', 'slick', 'watery', 'effervescent', 'fizzy', 'tingly', 'prickly', 'carbonation', 'viscosity', 'warming', 'coating', 'biting', 'sharp'],
    "brewing": [ 'dry hopping', 'double dry hopping', 'barrel-aged', 'bottle-conditioned', 'open fermentation', 'secondary fermentation', 'wort', 'mash, sparging', 'cold crashing', 'decoction', 'conditioning', 'lacto', 'yeast strain', 'adjuncts', 'grains', 'malt', 'specialty grains'],
    "technical": [ 'balance', 'complexity', 'depth', 'layers', 'nuanced', 'refined', 'structured', 'profile', 'round', 'harmonious', 'clean', 'crisp', 'finish', 'lingering', 'evolving', 'sharp', 'clarity', 'purity', 'dense', 'robust', 'powerful', 'light', 'restrained', 'vibrant', 'subdued', 'heavy', 'integrity', 'layered', 'exemplar', 'benchmark', 'classic', 'signature style', 'finesse', 'elegance'],
    "appearance": ['hazy', 'cloudy', 'opaque', 'translucent', 'clear', 'bright', 'unfiltered', 'filtered', 'lacing', 'foam', 'frothy', 'rocky head', 'stable head', 'head retention', 'appearance', 'golden', 'amber', 'ruby', 'copper', 'dark', 'black', 'mahogany', 'light', 'straw', 'yellow', 'chestnut', 'tan', 'off-white head' ],
    "judgment": [ 'exemplar', 'well-integrated', 'restrained', 'harmonious', 'round', 'classic example', 'benchmark', 'flawless', 'exceptional', 'outstanding', 'world-class', 'traditional', 'innovative', 'unconventional', 'unique', 'reference point', 'nuanced' ],
    "off_flavors": [ 'oxidized', 'metallic', 'cardboard', 'stale', 'sulfur', 'skunky', 'diacetyl', 'astringent', 'phenolic', 'acetaldehyde', 'DMS', 'cloying', 'solvent-like', 'overly bitter', 'thin', 'harsh', 'vegetal', 'buttery', 'musty, moldy', 'medicinal' ],
    "miscellaneous": [ 'initial impression', 'mid-palate', 'aftertaste', 'finish', 'lingering', 'mouth-coating', 'evolving flavor', 'balanced start', 'unfolding', 'developing', 'peak', 'bright finish', 'dry finish', 'clean ending', 'reminiscent', 'similar to', 'akin to', 'comparable', 'surpasses', 'diverges from', 'evokes', 'hints of', 'resembles', 'distinct from', 'notes of', 'echoes' ]
    }

def get_exp_stems(expert_terms):
    expert_terms_stemmed = {}
    for category, terms in expert_terms.items():
        tokens = [word_tokenize(term.lower()) for term in terms]
    
        stemmer = PorterStemmer()
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
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    stems_ba = pd.read_pickle(os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    rb_dir = os.path.join(data_path, 'RateBeer')
    stems_rb = pd.read_pickle(os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
    
    expert_terms_stemmed = get_exp_stems(expert_terms)


    df_ba = score_df(stems_ba, expert_terms_stemmed) 
    df_ba.to_pickle(os.path.join(advocate_dir, 'reviews_w_scores.pkl'))

    df_rb = score_df(stems_rb, expert_terms_stemmed)
    df_rb.to_pickle(os.path.join(rb_dir, 'reviews_w_scores.pkl'))
