from scipy.stats import pearsonr
import pandas as pd
import numpy as np
import os

def get_expert_metric_dfs(data_path):
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')

    rev_with_scores = pd.read_pickle(os.path.join(advocate_dir, 'rev_w_scores.pkl'))
    rev_with_scores.columns = ['appearance_rt' if i == 9 else col for i, col in enumerate(rev_with_scores_rb.columns)]
    beers = pd.read_csv(os.path.join(advocate_dir, 'beers_BA_clean.csv'))
    users = pd.read_csv(os.path.join(advocate_dir, 'users_BA_clean.csv'))

    rev_with_scores['date'] =  pd.to_datetime(rev_with_scores['date'])
    users['date_first_review'] = pd.to_datetime(users['date_first_review'])

    # create a new column with the number of reviews each user gave
    rev_with_scores_grouped=rev_with_scores.groupby('user_id')['beer_id'].agg(['size'])
    rev_with_scores_grouped=rev_with_scores_grouped.reset_index()
    rev_with_scores_grouped=rev_with_scores_grouped.rename(columns={'size': 'nbr_reviews'})
    users= pd.merge(users, rev_with_scores_grouped, on="user_id")

    return rev_with_scores, beers, users

def parse_users(rev_with_scores):
    col_to_keep = ['flavor', 'mouthfeel', 'brewing', 'technical', 'appearance','off_flavors', 'expertness_score']
    user_ba = rev_with_scores.groupby('user_id').agg(
        {col: 'mean' for col in col_to_keep} | {'user_id': 'count'}
    )
    user_ba = user_ba.rename(columns={'user_id': 'nbr_rev'})

    return user_ba

def first_reviews(df, max=200):
    """
    Returns the earliest reviews for each user, up to a specified maximum.

    Parameters
    ----------
    df : DataFrame containing user review data, with 'user_id' and 'date' columns.
    max : Maximum number of reviews to return per user (default is 200).

    Returns
    -------
    DataFrame containing up to `max` earliest reviews per user, sorted by 'user_id' and 'date'.
    """

    df = df.sort_values(by=['user_id', 'date'])
    return df.groupby('user_id').head(max)

def joined_date_zero(reviews):
    """
    Normalizes review dates to the first review date for each user, setting their first review as day zero.

    Parameters
    ----------
    reviews : DataFrame containing user review data, with columns 'user_id' and 'date' (assumed to be datetime).

    Returns
    -------
        DataFrame where each user's review dates are adjusted relative to their first review date, 
        so that the first review date for each user is zero.
    """
    fir_rev = first_reviews(reviews, max=1).rename(columns={'date': 'first_date'})
    reviews = reviews.merge(fir_rev[['user_id', 'first_date']], on='user_id')
    reviews['date'] = reviews['date'] - reviews['first_date'] 
    reviews = reviews.drop(columns=['first_date'])
    return reviews

def standardize(x, y, cols):
    """
    Standardizes specified columns in DataFrame `x` based on means and standard deviations in DataFrame `y`.

    Parameters
    ----------
    x : DataFrame containing data to standardize, with 'beer_id' and columns to be standardized.
    y : DataFrame with 'beer_id' and statistical information for standardization, including means and standard deviations.
    cols : List of column names to standardize in `x`.

    Returns
    -------
        DataFrame `x` with specified columns standardized.
    """
    y_copy = y.drop(columns=['review_count'])
    y_copy.columns = ['beer_id'] + [f"{col}_{stat}" for col in cols for stat in ['mean', 'std']]

    x = x.merge(y_copy, on='beer_id')

    for col in cols:
        std = x[f"{col}_std"]
        x[col] = np.where(std != 0, (x[col] - x[f"{col}_mean"]) / std, x[col] - x[f"{col}_mean"])

    x = x.drop(columns=[f"{col}_mean" for col in cols])

    return x

def corr_and_count(group, att_1='expertness_score', replace_date=False):
    """
    Calculates the correlation between att_1 and 'date' within a given group, 
    along with the count of 'date' entries.

    Parameters
    ----------
    group :  A DataFrame group with columns att_1 and 'date'.
    att_1 : name of the first column
    replace_date : bool if True replace the date with an incremental counter

    Returns
    -------
    A Series containing:
        - 'correlation': The correlation between att_1 and 'date'. If the standard deviation 
          of either column is zero, the correlation is set to NaN.
        - 'total_count': The count of non-NaN entries in the 'date' column.

    """
    if(replace_date):
        group = group.sort_values(by='date')
        group['date'] = range(len(group))
        
    count = group['date'].count()
    if group[att_1].std() == 0 or group['date'].std() == 0 or len(group['date'])<2:
        correlation= float('nan') 
        p_value = float('nan')
    else:
        correlation, p_value = pearsonr(group[att_1], group['date'])
    
    return pd.Series({'correlation': correlation,'p_value': p_value,  'total_count': count})

def review_of_experts(df, users, nbr_rev=100):
    x = df.merge(users[['user_id','nbr_reviews']], on='user_id')
    return x[x['nbr_reviews']>nbr_rev]

def get_scores_for_beer(rev_with_scores, col_to_keep):
    scores_for_beer = rev_with_scores.groupby('beer_id').agg(
        {col: ['mean', 'std'] for col in col_to_keep} | {'beer_id': 'count'}
    )

    scores_for_beer = scores_for_beer.rename(columns={'beer_id': 'review_count'})
    scores_for_beer = scores_for_beer[scores_for_beer['review_count']['count']>1]
    return scores_for_beer