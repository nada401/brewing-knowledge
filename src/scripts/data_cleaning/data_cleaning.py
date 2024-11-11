from datetime import datetime
import pandas as pd
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

    
# Applica la trasformazione solo se il valore non è NaN
   users['joined'] = users['joined'].apply(lambda data_seconds: datetime.fromtimestamp(data_seconds).date() if pd.notna(data_seconds) else data_seconds)

   users['joined'] =pd.to_datetime(users['joined'])
   users['user_id'] = users['user_id'].astype(object)
   

   return users




    