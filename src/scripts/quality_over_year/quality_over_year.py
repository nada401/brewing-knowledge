import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def order_months(df):
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    df['month_order'] = df.index.map(month_order)

    return df.sort_values('month_order').drop(columns='month_order')

def reviews_per_month(df):
    number_of_reviews_month = df.groupby('month').size()
    number_of_reviews_month = number_of_reviews_month.reset_index(name='review_count')

    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    number_of_reviews_month['month'] = pd.Categorical(
        number_of_reviews_month['month'], categories=month_order, ordered=True
    )

    return number_of_reviews_month.sort_values('month')

def review_per_day(df):
    temp = df.groupby('day').size().copy() # necessary?
    return pd.Categorical(temp['day'], ordered=True)

def get_oktoberfest_data(data_path):
    # Find breweries in Munich
    df_brew = pd.read_csv(os.path.join(data_path, 'RateBeer/breweries_RB_clean.csv'))
    df_score = pd.read_pickle(os.path.join(data_path, 'RateBeer/rev_w_scores.pkl'))

    # List of official breweries at Oktoberfest
    oktoberfest_breweries = ['Augustiner-Bräu', 'Hacker-Pschorr', 'Hofbräu München', 'Löwenbräu Munich', 'Paulaner', 'Spaten']
    
    # Check for matches (case-insensitive)
    ids_okt = df_brew[
        df_brew['name'].str.contains('|'.join(oktoberfest_breweries), case=False, na=False)
    ].id.to_list()

    df_score_okt = df_score[df_score['brewery_id'].isin(ids_okt)].copy()

    df_score_okt['date'] = pd.to_datetime(df_score_okt['date'])
    df_score_okt['year-month'] = df_score_okt['date'].dt.to_period('M')
    df_score_okt['month'] = df_score_okt['date'].dt.month_name()
    df_score_okt['day'] = df_score_okt['date'].dt.day

    df_score_exact = df_score_okt[
        ((df_score_okt['month'] == 'September') & (df_score_okt['day'] > 15)) |
        ((df_score_okt['month'] == 'October') & (df_score_okt['day'] <= 3))
    ]

    number_of_reviews_month = reviews_per_month(df_score_okt)

    mean_exp_oktoberfest = df_score_exact['expertness_score'].mean()
    mean_exp_year = df_score_okt['expertness_score'].mean()

    return number_of_reviews_month, mean_exp_oktoberfest, mean_exp_year

def plot_okt_n_review(rev_per_month):
    fig, ax = plt.subplots(figsize=(20, 8))
    color = 'brown'

    # Plot the line chart
    sns.lineplot(x='month', y='review_count', data=rev_per_month, ax=ax, color=color)

    # Add bigger dots on each data point
    sns.scatterplot(x='month', y='review_count', data=rev_per_month, ax=ax, 
                    color=color, s=200, label='Number of reviews', zorder=10)

    # Customize the chart
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel('Number of Reviews', fontsize=12)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylim(2000, 4250)
    ax.set_title('Number of Reviews per Month', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(fontsize=12)

def get_4july_data(data_path):
    df_score = pd.read_pickle(os.path.join(data_path, 'BeerAdvocate/rev_w_scores.pkl'))
    df_users = pd.read_csv(os.path.join(data_path, 'BeerAdvocate/users_BA_clean.csv'))

    # Take only users that are from the United States
    df_users = df_users[
        df_users['location'].str.contains('|'.join(['United States']), case=False, na=False)
    ]
    american_users = df_users.user_id.to_list()
    

    df_score_july = df_score.copy()
    df_score_july = df_score_july[df_score_july['user_id'].isin(american_users)]
    df_score_july['date'] = pd.to_datetime(df_score_july['date'])
    df_score_july['month'] = df_score_july['date'].dt.month_name()
    df_score_july['day'] = df_score_july['date'].dt.day

    df_score_july = df_score_july[df_score_july['month'] == 'July']

    df_score_year = df_score.copy()
    df_score_year = df_score_year[df_score_year['user_id'].isin(american_users)]
    df_score_year['date'] = pd.to_datetime(df_score_year['date'])
    df_score_year['month'] = df_score_year['date'].dt.month_name()

    exp_july = df_score_july.groupby('day')['expertness_score'].agg(['mean'])

    # Take the average of expertness score for all american users for the whole year and only the 4th of july
    df_americans = df_score[df_score['user_id'].isin(american_users)].copy()
    mean_exp_all = df_americans['expertness_score'].mean()
    mean_exp_4j = exp_july.loc[4]['mean']

    rev_july = df_score_july.groupby('day')['expertness_score'].agg(['size'])

    return rev_july, mean_exp_4j, mean_exp_all

def plot_4july_n_reviews(rev_july):
    plt.figure(figsize=(20, 8))
    plt.plot(rev_july.index, rev_july['size'], marker='o', linestyle='-', color='r', label='Number of reviews')
    plt.title('Reviews by Day (July)', fontsize=16)
    plt.xlabel('Day of July', fontsize=12)
    plt.ylabel('Number of reviews', fontsize=12)
    plt.ylim(5000, 7500)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

def get_stPatrick_data(data_path):
    df_score = pd.read_pickle(os.path.join(data_path, 'RateBeer/rev_w_scores.pkl'))

    # This takes the official Guinness breweries, and other with the name "Guinness
    df_score_guinness = df_score[df_score['brewery_name'].str.contains('|'.join(['Guinness', 'St. James']), case=False)].copy()
    df_score_guinness['date'] = pd.to_datetime(df_score_guinness['date'])
    df_score_guinness['month'] = df_score_guinness['date'].dt.month_name()
    df_score_guinness['day'] = df_score_guinness['date'].dt.day

    exp_guinness_march = df_score_guinness[df_score_guinness['month'] == 'March'].groupby('day')['expertness_score'].agg(['mean'])

    # Take the expertness score for the 17th of March and the mean over the whole year
    mean_exp_all = df_score_guinness['expertness_score'].mean()
    mean_exp_stP = exp_guinness_march.loc[17]['mean']

    return mean_exp_all, mean_exp_stP