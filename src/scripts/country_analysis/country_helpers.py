import pickle as pkl
import pandas as pd

def get_exp_scores(data_path):
  
    with open(data_path, "rb") as f:
        temp_df = pkl.load(f)

    temp_df = pd.DataFrame(temp_df)
    for criterion in temp_df.keys():
        temp_df[criterion + '_score'] = temp_df['stems'].apply(lambda cell: len(list(set(cell) & set(temp_df[criterion]))))
    
    return temp_df


def get_average_scores_time(df):
    # Copy the dataset
    merged_reviews = df.copy()

    # Normalize location names
    merged_reviews['location'] = merged_reviews['location'].str.replace(
        r'^United States, .*$', 'United States', regex=True)

    merged_reviews['location'] = merged_reviews['location'].replace(
        ['England', 'Northern Ireland', 'Scotland', 'Wales'], 'United Kingdom'
    )

    merged_reviews = merged_reviews[merged_reviews['location'].isin(filtered_reviews.location.unique())]
    merged_reviews['date'] = pd.to_datetime(merged_reviews['date'])

    # Extract the year from the 'date' column
    merged_reviews['year'] = merged_reviews['date'].dt.year

    # Proceed with filtering and grouping by location and year
    #filtered_reviews = (
    #    merged_reviews.groupby('location')
    #    .filter(lambda x: len(x) >= 5000)
    #)

    average_scores_time = (
        merged_reviews.groupby(['location', 'year'])['expert_score']
        .mean()
        .reset_index()
    )
    # average_scores_time = average_scores_time[average_scores_time.year >= 2000]
    average_scores_time = average_scores_time.sort_values(by='expert_score', ascending=False)
    
    return average_scores_time

def get_average_scores(df):
    merged_reviews = df.copy()

    merged_reviews['location'] = merged_reviews['location'].str.replace(
        r'^United States, .*$', 'United States', regex=True)
    merged_reviews['location'] = merged_reviews['location'].replace(
        ['England', 'Northern Ireland', 'Scotland', 'Wales'], 'United Kingdom'
    )

    user_review_counts = (
        merged_reviews.groupby(['location', 'user_id'])
        .size()
        .reset_index(name='review_count')
    )

    locations_with_sufficient_users = (
        user_review_counts[user_review_counts['review_count'] > 10]
        .groupby('location')['user_id']
        .nunique()
        .reset_index(name='num_users')
        .query('num_users >= 100')['location']
    )


    filtered_reviews = merged_reviews[
        merged_reviews['location'].isin(locations_with_sufficient_users)
    ]

    average_scores = (
        filtered_reviews.groupby('location')['expert_score']
        .mean()
        .reset_index()
    )

    average_scores = average_scores.sort_values(by='expert_score', ascending=False)

    return average_scores