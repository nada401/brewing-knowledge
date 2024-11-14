import pandas as pd
import os

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

def exp_term_score(text):
    scores = {category: 0 for category in expert_terms}

    # Count occurrences of terms in each category
    for category, terms in expert_terms.items():
        for term in terms:
            if term in text:
                scores[category] += 1  # Accumulate count for the category
    scores["expertness_score"] = sum(scores.values())
    return scores

def score_df(x):
    x = x.copy()
    x.loc[:, 'text_lower'] = x['text'].str.lower()
    scores =  x['text_lower'].apply(exp_term_score).apply(pd.Series)
    x = x.drop(columns=['text_lower'])
    return pd.concat([x, scores], axis=1)

def add_ex_score_BA (data_path):
    """
    Adds experience-based scores to BeerAdvocate review data and saves the result to a CSV file.

    Parameters:
    ----------
    data_path : str
        The path to the root directory containing the 'BeerAdvocate' folder with review data.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the filtered and processed reviews with experience scores.

    Notes:
    -----
    - This function reads review data from 'ratings_BA_clean.csv' in the 'BeerAdvocate' directory.
    - It filters reviews marked as 'True' for 'review' status.
    - The function applies the `score_df` function to add experience-based scores to each review.
    - The processed DataFrame is saved as 'reviews_with_exp_scores.csv' in the 'BeerAdvocate' directory.
    
    Example:
    -------
    >>> add_ex_score_BA('/path/to/data')
    """
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    reviews_ba = pd.read_csv(os.path.join(advocate_dir, 'ratings_BA_clean.csv'))

    print("review_BA_clea.csv read!")

    rev_true = reviews_ba[reviews_ba['review']==True][['user_id', 'beer_id', 'date', 'text']]
    
    print("Starting to calculate the scores!")

    rev_true = score_df(rev_true)

    print("Saving results to a csv!")

    rev_true.to_csv(os.path.join(advocate_dir, 'reviews_with_exp_scores.csv'))

    print("DONE!")