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
    exp_stem_set = []
    for category, terms in expert_terms.items():
        tokens = [word_tokenize(term.lower()) for term in terms]
    
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(word[0]) for word in tokens]
        exp_stem_set = exp_stem_set + stemmed_tokens
    
    return set(exp_stem_set)

def extract_keywords(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punkt_symbols = set(punctuation)
    removable_words= stop_words.union(punkt_symbols)

    filtered_tokens = [word for word in tokens if ((word not in removable_words) and word.isalpha())]

    # Stemming
    stemmer = PorterStemmer()
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

    exp_stem_set = get_exp_stems(expert_terms)


    rev_true_ba = stem_df(rev_true_ba, exp_stem_set) 
    rev_true_ba.to_pickle(os.path.join(advocate_dir, 'reviews_with_exp_stems.pkl'))

    rev_true_rb = stem_df(rev_true_rb, exp_stem_set)
    rev_true_rb.to_pickle(os.path.join(rb_dir, 'reviews_with_exp_stems.pkl'))
