import os
import pandas as pd

def load_dataframes(datapath):
    # Nomi dei file CSV nelle rispettive cartelle
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
    users_RB_path = os.path.join(datapath_rate_beer, breweries_RB_file_name)
    rating_RB_path = os.path.join(datapath_rate_beer, ratings_RB_file_name)
    tagged_RB_path = os.path.join(datapath_rate_beer, tagged_RB_file_name)

    beers_BA_path = os.path.join(datapath_beer_advocade, beers_BA_file_name)
    breweries_BA_path = os.path.join(datapath_beer_advocade, breweries_BA_file_name)
    users_BA_path = os.path.join(datapath_beer_advocade, breweries_BA_file_name)
    rating_BA_path = os.path.join(datapath_beer_advocade, ratings_BA_file_name)
    tagged_BA_path = os.path.join(datapath_beer_advocade, tagged_BA_file_name)

    

    # Carica i file CSV in DataFrames
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