import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import math
import os



def get_scores_for_beers(rev_with_scores, exp_categories):
    """
    Computes mean, standard deviation, and review count for beers based on specified categories.
    Parameters:
    -----------
    rev_with_scores : pandas.DataFrame
        A DataFrame containing beer reviews with scores. It must include a 'beer_id' column
        and other columns corresponding to expected scoring categories.
    
    exp_categories : list of str
        A list of column names representing the scoring categories (e.g., 'aroma', 'appearance', etc.)
        to include in the aggregation process.

    Returns:
    --------
    scores_for_beer : pandas.DataFrame
        A DataFrame indexed by 'beer_id' containing the following:
            - Mean and standard deviation for each specified category.
            - A 'review_count' column indicating the number of reviews for each beer.
        Only beers with more than one review are included.
    """
    col_to_keep = ['beer_id'] + exp_categories
    scores_for_beer = rev_with_scores.groupby('beer_id').agg(
        {col: ['mean', 'std'] for col in col_to_keep} | {'beer_id': 'count'}
    )

    scores_for_beer = scores_for_beer.rename(columns={'beer_id': 'review_count'})
    scores_for_beer = scores_for_beer[scores_for_beer['review_count']['count']>1]
    return scores_for_beer


def get_min_max_for_beers(rev_with_scores, exp_categories, threshold=1):
    """
    Computes the minimum and maximum scores for beers based on specified categories, 
    with an optional review count filter.

    Parameters:
    -----------
    rev_with_scores : pandas.DataFrame
        A DataFrame containing beer reviews with scores. It must include a 'beer_id' column
        and other columns corresponding to expected scoring categories.

    exp_categories : list of str
        A list of column names representing the scoring categories (e.g., 'aroma', 'appearance', etc.)
        to include in the aggregation process.

    rev_count : bool, optional (default=True)
        If True, includes a 'review_count' column indicating the number of reviews for each beer
        and filters out beers with only one review.

    Returns:
    --------
    scores_for_beer : pandas.DataFrame
        A DataFrame indexed by 'beer_id' containing the following:
            - Minimum and maximum scores for each specified category.
            - If `rev_count` is True, a 'review_count' column indicating the number of reviews for each beer.
        Only beers with more than one review are included when `rev_count` is True.
    """
    col_to_keep = ['beer_id'] + exp_categories
    rev_gruoped = rev_with_scores[col_to_keep].groupby('beer_id')

    scores_for_beer = rev_gruoped.agg(
        {col: ['min', 'max'] for col in col_to_keep} | {'beer_id': 'count'}
    )
    scores_for_beer = scores_for_beer.rename(columns={'beer_id': 'review_count'})
    scores_for_beer = scores_for_beer[scores_for_beer['review_count', 'count']>=threshold]


    return scores_for_beer

def get_min_max_for_style(rev_with_scores, exp_categories):
    col_to_keep = ['style'] + exp_categories
    style_group = rev_with_scores[col_to_keep].groupby('style')

    scores_style = style_group.agg(['min', 'max'])

    return scores_style.reset_index()

def get_mean_scores_beer(rev_with_scores, exp_categories):
    col_to_keep = ['beer_id'] + exp_categories
    mean_scores_beer = rev_with_scores.groupby('beer_id').agg({col: 'mean' for col in col_to_keep} | {'beer_id': 'count'})
    mean_scores_beer =mean_scores_beer.rename(columns={'beer_id': 'review_count'})
    return mean_scores_beer

def get_beer_gr(rev, beers, exp_categories):
    mean_scores_beer = get_mean_scores_beer(rev, exp_categories)
    complete_beer = pd.merge(beers, mean_scores_beer[mean_scores_beer['review_count']>=10], on='beer_id')
    col_to_keep = ['style'] + exp_categories
    return complete_beer[col_to_keep].groupby('style').mean()

def get_users_stats(rev_with_scores, exp_categories, user_id='user_id'):
    col_to_keep = [user_id] + exp_categories
    users = rev_with_scores.groupby(user_id).agg(
        {col: 'mean' for col in col_to_keep} | {user_id: 'count'}
    )

    users = users.rename(columns={user_id: 'nbr_rev'})
    return users

def first_reviews(df,user_id='user_id', max=200):
    """
    Returns the earliest reviews for each user, up to a specified maximum.

    Parameters
    ----------
    df : DataFrame containing user review data, with user_id and 'date' columns.
    max : Maximum number of reviews to return per user (default is 200).

    Returns
    -------
    DataFrame containing up to `max` earliest reviews per user, sorted by user_id and 'date'.
    """

    df = df.sort_values(by=[user_id, 'date'])
    return df.groupby(user_id).head(max)

def joined_date_zero(reviews, user_id='user_id'):
    """
    Normalizes review dates to the first review date for each user, setting their first review as day zero.

    Parameters
    ----------
    reviews : DataFrame containing user review data, with columns user_id and 'date' (assumed to be datetime).

    Returns
    -------
        DataFrame where each user's review dates are adjusted relative to their first review date, 
        so that the first review date for each user is zero.

    Example
    -------
    >>> joined_date_zero(reviews)
    """
    fir_rev = first_reviews(reviews, max=1).rename(columns={'date': 'first_date'})
    reviews = reviews.merge(fir_rev[[user_id, 'first_date']], on=user_id)
    reviews['date'] = reviews['date'] - reviews['first_date'] 
    reviews = reviews.drop(columns=['first_date'])
    return reviews

def standardize_log(x, cols, by_style=True,rev_nbr_thr=10, using_min=False):
    """
    Standardizes specified columns in DataFrame `x` based on min and max score for each beer after +1 and logscaling.

    Parameters
    ----------
    x : DataFrame containing data to standardize, with 'beer_id' and columns to be standardized.
    cols : List of column names to standardize in `x`.

    Returns
    -------
        DataFrame `x` with specified columns standardized.
    """
    if by_style:
        max_min_beers = get_min_max_for_style(x, cols)
        merge_on = 'style'
    else:
        max_min_beers = get_min_max_for_beers(x, cols, threshold=rev_nbr_thr).drop(columns=('review_count', 'count')).reset_index()
        merge_on = 'beer_id'
        
    max_min_beers.columns = [merge_on] + [f"{col}_{stat}" for col in cols for stat in ['min', 'max']]

    x = x.merge(max_min_beers, on=merge_on)

    for col in cols:
        min_ = x[f'{col}_min'].apply(lambda val: math.log(val + 1)) if using_min else 0
        max_ = x[f'{col}_max'].apply(lambda val: math.log(val + 1))
        
        x[col] = np.where(min_ == max_, 0, (x[col].apply(lambda val: math.log(val + 1)) - min_) / (max_ - min_))

    x = x.drop(columns=[f"{col}_min" for col in cols] + [f"{col}_max" for col in cols])

    return x

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

    x = x.drop(columns=[f"{col}_mean" for col in cols] + [f"{col}_std" for col in cols])

    return x

def review_of_experts(df, users, user_id='user_id', nbr_rev=100, max_rev=100000):
    x = df.merge(users[[user_id,'nbr_reviews']], on=user_id)
    return x[(x['nbr_reviews']>=nbr_rev) & (x['nbr_reviews']<=max_rev)]

def get_avg_rev(rev, exp_categories):
    avg_rev = rev.sort_values(by=['user_id', 'date'])
    avg_rev['rev_nbr'] = avg_rev.groupby('user_id').cumcount()
    avg_rev = avg_rev.drop(columns=['date'])
    col_to_keep = ['rev_nbr'] + exp_categories
    return avg_rev[col_to_keep].groupby('rev_nbr').agg(['mean', ('sem', lambda x: x.sem())])


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
        correlation, p_value = pearsonr(group[att_1], group['date'].astype(int))
    
    return pd.Series({'correlation': correlation,'p_value': p_value,  'total_count': count})

def get_complete_rev(rev, users, user_id='user_id'):
    complete_exp_rev = pd.merge(rev, users[[user_id, 'location']], on=user_id)
    complete_exp_rev = complete_exp_rev.sort_values(by=[user_id, 'date'])

    # Create incremental numbers for each user
    complete_exp_rev['rev_nbr'] = complete_exp_rev.groupby(user_id).cumcount() 
    complete_exp_rev['location'] = complete_exp_rev['location'].str.replace(r'United States, .*', 'United States', regex=True)
    return complete_exp_rev

def get_expert_metric_dfs(data_path):
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    rb_dir = os.path.join(data_path, 'RateBeer')

    
    rev_with_scores_ba = pd.read_pickle(os.path.join(advocate_dir, 'rev_w_scores.pkl'))
    rev_with_scores_ba['date'] = pd.to_datetime(rev_with_scores_ba['date'])
    rev_with_scores_rb = pd.read_pickle(os.path.join(rb_dir, 'rev_w_scores.pkl'))
    rev_with_scores_rb['date'] = pd.to_datetime(rev_with_scores_rb['date'])


    beers_ba = pd.read_csv(os.path.join(advocate_dir, 'beers_BA_clean.csv'))
    users_ba = pd.read_csv(os.path.join(advocate_dir, 'users_BA_clean.csv'))
    beers_rb = pd.read_csv(os.path.join(rb_dir, 'beers.csv'))
    users_rb = pd.read_csv(os.path.join(rb_dir, 'users_RB_clean.csv'))
    return rev_with_scores_ba, beers_ba, users_ba, rev_with_scores_rb, beers_rb, users_rb 

def get_corr_df(rev, users, user_id='user_id', nbr_rev=50, at_least=200):
    rev_of_exp = review_of_experts(rev, users,nbr_rev=at_least)
    sel_rev_of_exp = first_reviews(rev_of_exp, user_id, max=nbr_rev)
    result_rep_date = sel_rev_of_exp.groupby(user_id).apply(lambda group: corr_and_count(group, replace_date=True), include_groups=False)
    return result_rep_date.dropna()

def get_first_rev_by_user(rev_std, users, user_id='user_id',max=5):
    rev = review_of_experts(rev_std, users)
    rev_grouped = first_reviews(rev, max=max).groupby(user_id)[['expertness_score']].agg('mean')
    return rev_grouped

def get_exp_levels(rev_std_grouped):
    exp_levels={}
    threshold_20 = rev_std_grouped['expertness_score'].quantile(0.2)
    exp_levels['Bottom 20%'] = rev_std_grouped[rev_std_grouped['expertness_score'] < threshold_20].index

    threshold_80 = rev_std_grouped['expertness_score'].quantile(0.8)
    exp_levels['Top 20%'] = rev_std_grouped[rev_std_grouped['expertness_score'] >= threshold_80].index

    exp_levels['20-80%'] = rev_std_grouped[
        (rev_std_grouped['expertness_score'] >= threshold_20) & 
        (rev_std_grouped['expertness_score'] < threshold_80)
    ].index
    return exp_levels

def get_complete_rev(rev, users, user_id='user_id'):
    complete_exp_rev = pd.merge(rev, users[[user_id, 'location']], on=user_id)
    complete_exp_rev = complete_exp_rev.sort_values(by=[user_id, 'date'])

    # Create incremental numbers for each user
    complete_exp_rev['rev_nbr'] = complete_exp_rev.groupby(user_id).cumcount() 
    complete_exp_rev['location'] = complete_exp_rev['location'].str.replace(r'United States, .*', 'United States', regex=True)
    return complete_exp_rev

def get_expert_metric_dfs(data_path):
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')
    rb_dir = os.path.join(data_path, 'RateBeer')

    
    rev_with_scores_ba = pd.read_pickle(os.path.join(advocate_dir, 'rev_w_scores.pkl'))
    rev_with_scores_ba['date'] = pd.to_datetime(rev_with_scores_ba['date'])
    rev_with_scores_rb = pd.read_pickle(os.path.join(rb_dir, 'rev_w_scores.pkl'))
    rev_with_scores_rb['date'] = pd.to_datetime(rev_with_scores_rb['date'])


    beers_ba = pd.read_csv(os.path.join(advocate_dir, 'beers_BA_clean.csv'))
    users_ba = pd.read_csv(os.path.join(advocate_dir, 'users_BA_clean.csv'))
    beers_rb = pd.read_csv(os.path.join(rb_dir, 'beers.csv'))
    users_rb = pd.read_csv(os.path.join(rb_dir, 'users_RB_clean.csv'))
    return rev_with_scores_ba, beers_ba, users_ba, rev_with_scores_rb, beers_rb, users_rb 

def get_corr_df(rev, users, user_id='user_id', nbr_rev=50, at_least=200):
    rev_of_exp = review_of_experts(rev, users,nbr_rev=at_least)
    sel_rev_of_exp = first_reviews(rev_of_exp, user_id, max=nbr_rev)
    result_rep_date = sel_rev_of_exp.groupby(user_id).apply(lambda group: corr_and_count(group, replace_date=True), include_groups=False)
    return result_rep_date.dropna()

def get_first_rev_by_user(rev_std, users, user_id='user_id',max=5):
    rev = review_of_experts(rev_std, users)
    rev_grouped = first_reviews(rev, max=max).groupby(user_id)[['expertness_score']].agg('mean')
    return rev_grouped

def get_exp_levels(rev_std_grouped):
    exp_levels={}
    threshold_20 = rev_std_grouped['expertness_score'].quantile(0.2)
    exp_levels['Bottom 20%'] = rev_std_grouped[rev_std_grouped['expertness_score'] < threshold_20].index

    threshold_80 = rev_std_grouped['expertness_score'].quantile(0.8)
    exp_levels['Top 20%'] = rev_std_grouped[rev_std_grouped['expertness_score'] >= threshold_80].index

    exp_levels['20-80%'] = rev_std_grouped[
        (rev_std_grouped['expertness_score'] >= threshold_20) & 
        (rev_std_grouped['expertness_score'] < threshold_80)
    ].index
    return exp_levels

def plot_exp_countries_evolution(
    rev, users, exp_levels, exp_categories,
    eng_countries, user_id='user_id', max_rev=1000
):
    # Preprocessing steps
    sel_rev = first_reviews(review_of_experts(rev, users, nbr_rev=5), user_id=user_id,max=max_rev)

    complete = get_complete_rev(sel_rev, users, user_id=user_id)

    # Grouping by country
    countries = {'English - ': complete['location'].isin(eng_countries),
         'Not English - ': ~complete['location'].isin(eng_countries)}
    
    colors = {'Bottom 20%': 'blue', 'Top 20%': 'green', '20-80%': 'orange'}

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=200, sharex=True, sharey=True)
    fig.suptitle("%s - Evolution of Expertness Score by Group" %('BeerAdvocate' if user_id=='user_id' else 'RateBeer'), fontsize=16)


    # Plotting
    for key_l in exp_levels.keys():
        for i, key_c in enumerate(countries.keys()):
            avg_rev = get_avg_rev(
                complete[(complete[user_id].isin(exp_levels[key_l])) & countries[key_c]],
                exp_categories
            )

            axes[i].plot(
                avg_rev.index, avg_rev['expertness_score']['mean'],
                label=f"{key_l} - Mean", color=colors[key_l]
            )
            axes[i].fill_between(
                avg_rev.index,
                avg_rev['expertness_score']['mean'] - avg_rev['expertness_score']['sem'],
                avg_rev['expertness_score']['mean'] + avg_rev['expertness_score']['sem'],
                color=colors[key_l], alpha=0.2
            )
            axes[i].set_title(f"{key_c}")
            axes[i].grid(True)
            axes[i].legend()
            axes[i].set_xlabel('Review Count')
            axes[i].set_ylabel('Expertness Score')
    plt.show()

def plot_exp_level_evolution(
    rev_std_ba, rev_std_rb, users_ba, users_rb,
    exp_levels_ba, exp_levels_rb, exp_categories, max_rev=1000
):
    # Preprocessing steps
    rev_ba = first_reviews(review_of_experts(rev_std_ba, users_ba, nbr_rev=5), max=max_rev)
    rev_rb = first_reviews(review_of_experts(rev_std_rb, users_rb, nbr_rev=5), user_id='user_name',max=max_rev)


    colors = {'Bottom 20%': 'blue', 'Top 20%': 'green', '20-80%': 'orange'}

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=200, sharex=True, sharey=True)
    fig.suptitle("Evolution of Expertness Score by Group", fontsize=16)

    # Plotting
    for key_l in exp_levels_ba.keys():
        avg_rev_ba = get_avg_rev(rev_ba[rev_ba.user_id.isin(exp_levels_ba[key_l])], exp_categories)
        avg_rev_rb = get_avg_rev(rev_rb[rev_rb.user_name.isin(exp_levels_rb[key_l])],exp_categories)

        # Plot BeerAdvocate
        axes[0].plot(
            avg_rev_ba.index, avg_rev_ba['expertness_score']['mean'],
            label=f"{key_l} - Mean", color=colors[key_l]
        )
        axes[0].fill_between(
            avg_rev_ba.index,
            avg_rev_ba['expertness_score']['mean'] - avg_rev_ba['expertness_score']['sem'],
            avg_rev_ba['expertness_score']['mean'] + avg_rev_ba['expertness_score']['sem'],
            color=colors[key_l], alpha=0.2
        )
        axes[0].set_title("BeerAdvocate")
        axes[0].grid(True)
        axes[0].legend()
        axes[0].set_xlabel('Review Count')
        axes[0].set_ylabel('Expertness Score')

        # Plot RateBeer
        axes[1].plot(
            avg_rev_rb.index, avg_rev_rb['expertness_score']['mean'],
            label=f"{key_l} - Mean", color=colors[key_l]
        )
        axes[1].fill_between(
            avg_rev_rb.index,
            avg_rev_rb['expertness_score']['mean'] - avg_rev_rb['expertness_score']['sem'],
            avg_rev_rb['expertness_score']['mean'] + avg_rev_rb['expertness_score']['sem'],
            color=colors[key_l], alpha=0.2
        )
        axes[1].set_title("RateBeer")
        axes[1].legend()
        axes[1].grid(True)

    plt.show()

def plot_categorical_evolution(rev_std_ba, rev_std_rb, users_ba, users_rb, exp_categories):
    rev_ba = review_of_experts(rev_std_ba, users_ba, nbr_rev=5)
    rev_rb = review_of_experts(rev_std_rb, users_rb, user_id='user_name', nbr_rev=5)

    nbr_rev=1000
    rev_ba = first_reviews(rev_ba, max=nbr_rev)
    rev_rb = first_reviews(rev_rb, user_id='user_name', max=nbr_rev)

    avg_rev_ba = get_avg_rev(rev_ba, exp_categories)
    avg_rev_rb = get_avg_rev(rev_rb, exp_categories)
        
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), dpi=200, sharex=True, sharey=True)
    fig.suptitle("Evolution of Categorical Scores", fontsize=16)

    # Loop through each expertise group and calculate stats
    for key in exp_categories:
        if key=='expertness_score':
            continue
        
        # Plot the mean line
        axes[0].plot(
            avg_rev_ba.index,
            avg_rev_ba[key]['mean'],
            label=f"{key} - Mean",
        )

        # Plot the SEM as a shaded area
        axes[0].fill_between(
            avg_rev_ba.index,
            avg_rev_ba[key]['mean'] - avg_rev_ba[key]['sem'],
            avg_rev_ba[key]['mean'] + avg_rev_ba[key]['sem'],
            alpha=0.2,
            label=f"{key} ± SEM"
        )

        axes[1].plot(
            avg_rev_rb.index,
            avg_rev_rb[key]['mean'],
            label=f"{key} - Mean",
        )

        axes[1].fill_between(
            avg_rev_rb.index,
            avg_rev_rb[key]['mean'] - avg_rev_rb[key]['sem'],
            avg_rev_rb[key]['mean'] + avg_rev_rb[key]['sem'],
            alpha=0.2,
            label=f"{key} ± SEM"
        )

    # Formatting for each subplot
    axes[0].set_title("BeerAdvocate")
    axes[0].set_xlabel('Review Count')
    axes[0].set_ylabel('Expertness Score')
    axes[0].grid(True)

    axes[1].set_title("RateBeer")
    axes[1].grid(True)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.1, 0.95), title='Legend')

    plt.show()

def plot_first_rev_distribution(rev_first_gr_ba, rev_first_gr_rb):
    fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=200, sharex=True) 

    fig.suptitle('Mean of the score (standardized) of the first 5 reviews per user')
    sns.histplot(rev_first_gr_ba.expertness_score, bins = 75, ax=axes[0])
    axes[0].set_title("BeerAdvocate")
    sns.histplot(rev_first_gr_rb.expertness_score, bins = 80, ax=axes[1])
    axes[1].set_title("RateBeer") 

    plt.tight_layout()  
    plt.show()

def plot_radar_chart(df, categories,angles, title):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=200, subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw one beer style per loop
    for beer in df.index:
        values = df.loc[beer].tolist()  # Get the values for the beer style
        values += values[:1]  # Complete the loop for each beer style
        ax.plot(angles, values, label=beer)
        ax.fill(angles, values, alpha=0.1)

    # Add labels for each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.yaxis.set_visible(False)

    # Add title and legend
    plt.title(title, size=15, color='darkblue', pad=20)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.show()

def plot_cat_score_per_style(beer_gr_ba, beer_gr_rb, exp_categories):
    normalized_beer_max_ba = pd.DataFrame()    
    normalized_beer_max_rb = pd.DataFrame()
    
    for col in exp_categories:
        if col =='expertness_score':
            continue
        if col == 'brewing':
            normalized_beer_max_ba = pd.concat([normalized_beer_max_ba, beer_gr_ba.loc[beer_gr_ba[col].idxmax():beer_gr_ba[col].idxmax()]])            
            normalized_beer_max_rb = pd.concat([normalized_beer_max_rb, beer_gr_rb.loc[beer_gr_rb[col].nlargest(2).idxmin():beer_gr_rb[col].nlargest(2).idxmin()]])
        else:
            normalized_beer_max_ba = pd.concat([normalized_beer_max_ba, beer_gr_ba.loc[beer_gr_ba[col].idxmax():beer_gr_ba[col].idxmax()]])            
            normalized_beer_max_rb = pd.concat([normalized_beer_max_rb, beer_gr_rb.loc[beer_gr_rb[col].idxmax():beer_gr_rb[col].idxmax()]])
    
    normalized_beer_max_ba = normalized_beer_max_ba / beer_gr_ba.max()
    normalized_beer_max_rb = normalized_beer_max_rb / beer_gr_rb.max()


    normalized_beer_max_ba = normalized_beer_max_ba.drop(columns='expertness_score')
    normalized_beer_max_rb = normalized_beer_max_rb.drop(columns='expertness_score')

    categories = ["Flavor", "Mouthfeel", "Brewing", "Technical", "Appearance", "Off flavors"]
    num_vars = len(categories)

    # Set up radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop

    plot_radar_chart(normalized_beer_max_ba, categories, angles, "BeerAdvocate - Comparison of Beer Styles Across Attributes")
    plot_radar_chart(normalized_beer_max_rb, categories, angles, "Ratebeer - Comparison of Beer Styles Across Attributes")


# Not used anymore to do the plot side by side
# def plot_exp_level_evolution(
#     rev_std_ba, rev_std_rb, users_ba, users_rb,
#     exp_levels_ba, exp_levels_rb, exp_categories,
#     eng_countries=None, max_rev=1000
# ):
#     # Preprocessing steps
#     rev_ba = first_reviews(review_of_experts(rev_std_ba, users_ba, nbr_rev=5), max=max_rev)
#     rev_rb = first_reviews(review_of_experts(rev_std_rb, users_rb, nbr_rev=5), user_id='user_name',max=max_rev)

#     complete_ba = get_complete_rev(rev_ba, users_ba)
#     complete_rb = get_complete_rev(rev_rb, users_rb, user_id='user_name',)

#     # Grouping by country
#     countries_ba = (
#         {'': True} if eng_countries is None else
#         {'English - ': complete_ba['location'].isin(eng_countries),
#          'Not English - ': ~complete_ba['location'].isin(eng_countries)}
#     )
#     countries_rb = (
#         {'': True} if eng_countries is None else
#         {'English - ': complete_rb['location'].isin(eng_countries),
#          'Not English - ': ~complete_rb['location'].isin(eng_countries)}
#     )

#     colors = {'Bottom 20%': 'blue', 'Top 20%': 'green', '20-80%': 'orange'}

#     len_c = len(countries_ba)
#     fig, axes = plt.subplots(nrows=len_c, ncols=2, figsize=(15, 6 * len_c), sharex=True, sharey=True)
#     fig.suptitle("Evolution of Expertness Score by Group", fontsize=16)

#     if len_c == 1:  # Handle single-row case
#         axes = [axes]

#     # Plotting
#     for key_l in exp_levels_ba.keys():
#         for i, key_c in enumerate(countries_ba.keys()):
#             avg_rev_ba = get_avg_rev(
#                 complete_ba[(complete_ba.user_id.isin(exp_levels_ba[key_l])) & countries_ba[key_c]],
#                 exp_categories
#             )
#             avg_rev_rb = get_avg_rev(
#                 complete_rb[(complete_rb.user_name.isin(exp_levels_rb[key_l])) & countries_rb[key_c]],
#                 exp_categories
#             )

#             # Plot BeerAdvocate
#             axes[i][0].plot(
#                 avg_rev_ba.index, avg_rev_ba['expertness_score']['mean'],
#                 label=f"{key_l} - Mean", color=colors[key_l]
#             )
#             axes[i][0].fill_between(
#                 avg_rev_ba.index,
#                 avg_rev_ba['expertness_score']['mean'] - avg_rev_ba['expertness_score']['sem'],
#                 avg_rev_ba['expertness_score']['mean'] + avg_rev_ba['expertness_score']['sem'],
#                 color=colors[key_l], alpha=0.2
#             )
#             axes[i][0].set_title(f"{key_c}BeerAdvocate")
#             axes[i][0].grid(True)
#             axes[i][0].legend()
#             axes[i][0].set_xlabel('Review Count')
#             axes[i][0].set_ylabel('Expertness Score')

#             # Plot RateBeer
#             axes[i][1].plot(
#                 avg_rev_rb.index, avg_rev_rb['expertness_score']['mean'],
#                 label=f"{key_l} - Mean", color=colors[key_l]
#             )
#             axes[i][1].fill_between(
#                 avg_rev_rb.index,
#                 avg_rev_rb['expertness_score']['mean'] - avg_rev_rb['expertness_score']['sem'],
#                 avg_rev_rb['expertness_score']['mean'] + avg_rev_rb['expertness_score']['sem'],
#                 color=colors[key_l], alpha=0.2
#             )
#             axes[i][1].set_title(f"{key_c}RateBeer")
#             axes[i][1].legend()
#             axes[i][1].grid(True)

#     plt.show()