import pandas as pd
import os

def get_expert_metric_dfs(data_path):
    advocate_dir = os.path.join(data_path, 'BeerAdvocate')

    rev_with_scores = pd.read_csv(os.path.join(advocate_dir, 'reviews_with_exp_scores.csv'))
    beers = pd.read_csv(os.path.join(advocate_dir, 'beers_BA_clean.csv'))
    users = pd.read_csv(os.path.join(advocate_dir, 'users_BA_clean.csv'))

    rev_with_scores['date'] =  pd.to_datetime(rev_with_scores['date'])
    users['date_first_review'] = pd.to_datetime(users['date_first_review'])

    rev_with_scores_grouped=rev_with_scores.groupby('user_id')['beer_id'].agg(['size'])
    rev_with_scores_grouped=rev_with_scores_grouped.reset_index()
    rev_with_scores_grouped=rev_with_scores_grouped.rename(columns={'size': 'nbr_reviews'})
    users= pd.merge(users, rev_with_scores_grouped, on="user_id")

    return rev_with_scores, beers, users
