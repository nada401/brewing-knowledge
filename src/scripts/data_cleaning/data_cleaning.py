from datetime import datetime
import pandas as pd
import os

def load_dataframes(datapath):
    # names of files and respective folders
    datapath_rate_beer = datapath+'/RateBeer'
    datapath_beer_advocade = datapath+'/BeerAdvocate'
    
    beers_RB_file_name = "beers.csv"  
    breweries_RB_file_name = "breweries.csv"
    users_RB_file_name = "users.csv"
    ratings_RB_file_name = "ratings_RB.csv"
    tagged_RB_file_name = "reviews_tagged.csv"

    beers_BA_file_name = "beers.csv"  
    breweries_BA_file_name = "breweries.csv"
    users_BA_file_name = "users.csv"
    ratings_BA_file_name = "ratings_BA.csv"
    ratings_BA_file_name = "ratings_BA.csv"
    tagged_BA_file_name =  "reviews_tagged.csv"
  

    beers_RB_path = os.path.join(datapath_rate_beer, beers_RB_file_name)
    breweries_RB_path = os.path.join(datapath_rate_beer, breweries_RB_file_name)
    users_RB_path = os.path.join(datapath_rate_beer, users_RB_file_name)
    rating_RB_path = os.path.join(datapath_rate_beer, ratings_RB_file_name)
    tagged_RB_path = os.path.join(datapath_rate_beer, tagged_RB_file_name)

    beers_BA_path = os.path.join(datapath_beer_advocade, beers_BA_file_name)
    breweries_BA_path = os.path.join(datapath_beer_advocade, breweries_BA_file_name)
    users_BA_path = os.path.join(datapath_beer_advocade, users_BA_file_name)
    rating_BA_path = os.path.join(datapath_beer_advocade, ratings_BA_file_name)
    tagged_BA_path = os.path.join(datapath_beer_advocade, tagged_BA_file_name)
    
    

    # load csv in dataFrames
    beer_RB = pd.read_csv(beers_RB_path)
    breweries_RB = pd.read_csv(breweries_RB_path)
    users_RB = pd.read_csv(users_RB_path)
    ratings_RB=pd.read_csv(rating_RB_path)
    tagged_RB=pd.read_csv(tagged_RB_path)

    beer_BA = pd.read_csv(beers_BA_path)
    breweries_BA = pd.read_csv(breweries_BA_path)
    users_BA = pd.read_csv(users_BA_path)
    ratings_BA =pd.read_csv(rating_BA_path)
    tagged_BA= pd.read_csv(tagged_BA_path)
   

    return beer_RB, breweries_RB, users_RB, ratings_RB, tagged_RB, beer_BA, breweries_BA, users_BA, ratings_BA, tagged_BA

def format_attribute_ratings(ratings):
   
    '''
    formatted  all attributes of ratings dataframe
    '''
    ratings['user_id'] = ratings['user_id'].astype(str)
    ratings['rating'] = ratings['rating'].astype(float)
    ratings['abv'] = ratings['abv'].astype(float)
    ratings['appearance'] = ratings['appearance'].astype(float)
    ratings['aroma'] = ratings['aroma'].astype(float)
    ratings['palate'] = ratings['palate'].astype(float)
    ratings['taste'] = ratings['taste'].astype(float)
    ratings['overall'] = ratings['overall'].astype(float)
    ratings['date'] = ratings['date'].astype(int)
    ratings['date'] = ratings['date'].apply(lambda data_seconds : datetime.fromtimestamp(data_seconds).date())
    ratings['date']=pd.to_datetime(ratings['date'])
    
    return ratings
    
def format_attribute_beers(beers):
   
    '''
    formatted  all attributes of beers dataframe
    '''

    beers['nbr_ratings'] = beers['nbr_ratings'].astype(int)
    beers['overall_score'] = beers['overall_score'].astype(float)
    beers['style_score'] = beers['style_score'].astype(float)
    beers['avg'] = beers['avg'].astype(float)
    beers['abv'] = beers['abv'].astype(float)
    beers['avg_computed']  = beers['avg_computed'].astype(float)
    beers['zscore'] = beers['zscore'].astype(float)
    beers['nbr_matched_valid_ratings'] = beers['nbr_matched_valid_ratings'].astype(int)
    beers['avg_matched_valid_ratings'] = beers['avg_matched_valid_ratings'].astype(float)
    
    return beers

def format_attribute_beers_BA(beers):
   
    '''
    formatted  all attributes of beers dataframe
    '''

    beers['nbr_ratings'] = beers['nbr_ratings'].astype(int)
    beers['avg'] = beers['avg'].astype(float)
    beers['abv'] = beers['abv'].astype(float)
    beers['avg_computed']  = beers['avg_computed'].astype(float)
    beers['zscore'] = beers['zscore'].astype(float)
    beers['nbr_matched_valid_ratings'] = beers['nbr_matched_valid_ratings'].astype(int)
    beers['avg_matched_valid_ratings'] = beers['avg_matched_valid_ratings'].astype(float)
    
    return beers

    
def format_attribute_breweries(brewery):
   
    '''
    formatted  attributes of brewerie dataframe
    '''
    brewery['nbr_beers']=brewery['nbr_beers'].astype(int)
   
    return brewery

def format_attribute_tagged(tagged):
    '''
    formatted  attributes of tagged
    '''
    tagged['user_id'] = tagged['user_id'].astype(str)
    tagged['date'] = tagged['date'].astype(int)
    tagged['date'] = tagged['date'].apply(lambda data_seconds : datetime.fromtimestamp(data_seconds).date())
    tagged['date']=pd.to_datetime(tagged['date'])

    return tagged

def format_attribute_users(users):

   # Executes the function only if the value is not NaN
   users['joined'] = users['joined'].apply(lambda data_seconds: datetime.fromtimestamp(data_seconds).date() if pd.notna(data_seconds) else data_seconds)

   users['joined'] =pd.to_datetime(users['joined'])
   users['user_id'] = users['user_id'].astype(object)
   

   return users

# Load the dataframes and format them
def load_formatted_dataframes(folder_path):

    beer_RB, breweries_RB, users_RB, ratings_RB, tagged_RB, beer_BA, breweries_BA, users_BA, ratings_BA, tagged_BA= load_dataframes(folder_path)

    ratings_RB = format_attribute_ratings(ratings_RB)
    ratings_BA = format_attribute_ratings(ratings_BA)

    breweries_RB = format_attribute_breweries(breweries_RB)
    breweries_BA = format_attribute_breweries(breweries_BA)

    tagged_BA=format_attribute_tagged(tagged_BA)
    tagged_RB=format_attribute_tagged(tagged_RB)    

    beer_RB = format_attribute_beers(beer_RB)
    beer_BA = format_attribute_beers_BA(beer_BA)

    users_RB = format_attribute_users(users_RB)
    users_BA = format_attribute_users(users_BA)

    return beer_RB, breweries_RB, users_RB, ratings_RB, tagged_RB, beer_BA, breweries_BA, users_BA, ratings_BA, tagged_BA

def drop_duplicates_in_dataframes(users_RB, tagged_RB, tagged_BA, ratings_RB):

    users_RB = users_RB.drop_duplicates(subset='user_id', keep='first')
    tagged_RB = tagged_RB.drop_duplicates(subset=['beer_id', 'date', 'user_id'], keep='first')
    tagged_BA = tagged_BA.drop_duplicates(subset=['beer_id', 'date', 'user_id'], keep='first')
    ratings_RB = ratings_RB.drop_duplicates(subset=['user_id', 'beer_id',  'date'], keep='first')

    return users_RB, tagged_RB, tagged_BA, ratings_RB

def delete_beers_with_no_reviews(df_ratings, df_beer):
    df_extract = df_beer[['beer_id', 'beer_name','brewery_id','brewery_name','style']]
    ratings_grouped_beer = df_ratings.groupby(['beer_id'])[['appearance', 'aroma', 'palate', 'taste', 'overall','rating','review']].agg(
        nbr_ratings=('overall', 'size'),
        nbr_reviews=('review', 'sum'),
        aroma_mean=('aroma', 'mean'),
        aroma_std=('aroma', 'std'),
        palate_mean=('palate', 'mean'),
        palate_std=('palate', 'std'),
        taste_mean=('taste', 'mean'),
        taste_std=('taste', 'std'),
        overall_mean=('overall', 'mean'),
        overall_std=('overall', 'std')
    )
    return pd.merge(df_extract, ratings_grouped_beer, left_on='beer_id', right_index=True, how="inner")

def delete_users_with_no_reviews_BA(df_ratings, df_users):

    ratings_group_by_user = df_ratings.groupby('user_id')[['date']].agg(
        nbr_ratings = ('date', 'size'),
        date_first_review = ('date', 'min')
    )

    df_users_cleaned = df_users[['user_id', 'user_name', 'joined','location']]

    return pd.merge(df_users_cleaned, ratings_group_by_user, left_on='user_id', right_index=True, how='inner')

def delete_users_with_no_reviews_RB(df_ratings, df_users):

    ratings_group_by_user = df_ratings.groupby('user_name')[['date']].agg(
        nbr_ratings = ('date', 'size'),
        date_first_review = ('date', 'min')
    )
    ratings_group_by_user = ratings_group_by_user.reset_index()

    df_users_cleaned = df_users[['user_id', 'user_name', 'joined','location']]

    return pd.merge(df_users_cleaned, ratings_group_by_user, left_on='user_name', right_on="user_name")


def save_dataframes(ratings_BA, beer_BA_merged, breweries_BA, users_BA_cleaned, ratings_RB, beer_RB_merged, breweries_RB, users_RB_cleaned, folder_path):

    beerAdvocate_dir = folder_path + '/BeerAdvocate'
    ratings_BA.to_csv(os.path.join(beerAdvocate_dir, 'ratings_BA_clean.csv'), index=False)
    beer_BA_merged.to_csv(os.path.join(beerAdvocate_dir, 'beers_BA_clean.csv'), index=False)
    breweries_BA.to_csv(os.path.join(beerAdvocate_dir, 'breweries_BA_clean.csv'), index=False)
    users_BA_cleaned.to_csv(os.path.join(beerAdvocate_dir, 'users_BA_clean.csv'), index=False)

    rateBeer_dir = folder_path + '/RateBeer'
    ratings_RB.to_csv(os.path.join(rateBeer_dir, 'ratings_RB_clean.csv'), index=False)
    beer_RB_merged.to_csv(os.path.join(rateBeer_dir, 'beers_RB_clean.csv'), index=False)
    breweries_RB.to_csv(os.path.join(rateBeer_dir, 'breweries_RB_clean.csv'), index=False)
    users_RB_cleaned.to_csv(os.path.join(rateBeer_dir, 'users_RB_clean.csv'), index=False)

#* Entry point
def clean_data(folder_path):
    # Load dataframes
    beer_RB, breweries_RB, users_RB, ratings_RB, tagged_RB, beer_BA, breweries_BA, users_BA, ratings_BA, tagged_BA= load_formatted_dataframes(folder_path)

    # Drop duplicate
    users_RB, tagged_RB, tagged_BA, ratings_RB = drop_duplicates_in_dataframes(users_RB, tagged_RB, tagged_BA, ratings_RB)

    # Add a boolean column 'review'. True if there is a valid textual review, False otherwise
    ratings_RB['review']=ratings_RB['text'].apply(lambda text: pd.notna(text) and str(text).strip() != '')
    ratings_BA['review']=ratings_BA['text'].apply(lambda text: pd.notna(text) and str(text).strip() != '')

    # If appearance	'aroma' 'palate' 'taste' 'overall' and 'review' are all False, delete the row
    ratings_BA = ratings_BA.dropna(subset=['appearance', 'aroma', 'palate', 'taste', 'overall', 'text'], how='all')

    # Delete beers with no reviews
    beer_RB_merged = delete_beers_with_no_reviews(ratings_RB ,beer_RB)
    beer_BA_merged = delete_beers_with_no_reviews(ratings_BA ,beer_BA)

    # Merge the cleaned dataframes with the tagged dataframes
    ratings_RB = pd.merge(ratings_RB, tagged_RB, left_on=['beer_id', 'date', 'user_id'],right_on=['beer_id', 'date', 'user_id'], how='left')
    ratings_BA = pd.merge(ratings_BA, tagged_BA, left_on=['beer_id', 'date', 'user_id'],right_on=['beer_id', 'date', 'user_id'], how='left')

    # Delete users with no reviews
    users_BA_cleaned = delete_users_with_no_reviews_BA(ratings_BA, users_BA)
    users_RB_cleaned = delete_users_with_no_reviews_RB(ratings_RB, users_RB)

    # Save cleaned dataframes
    save_dataframes(ratings_BA, beer_BA_merged, breweries_BA, users_BA_cleaned, ratings_RB, beer_RB_merged, breweries_RB, users_RB_cleaned, folder_path)
