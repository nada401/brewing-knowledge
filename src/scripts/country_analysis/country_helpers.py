import pickle as pkl
import pandas as pd

expert_terms =  {"flavor": ["caramel", "toffee", "bready", "biscuity", "nutty", "roasted", "chocolate", "coffee", "mocha", "molasses", "syrupy",
                          "smokey", "toasted", "vanilla", "cocoa", "sugar", "hoppy", "citrusy", "tropical", "floral", "piney",
                          "herbal", "grassy", "earthy", "dank", "spicy", "peppery", "juicy", "zesty", "tangy", "bitterness", "vinegar","lactic",
                          "estery", "farmyard","almond", "fruity", "berry", " cherry", " apple", " banana", "pear", "stone fruit", "plum", "fig",
                          "raisin", "peach", " apricot", "citrus zest", "lemon", "peel", "orange", "pineapple", "mango", "lychee", "oaky", "woody",
                          "bourbon", "whiskey", "rye", "tequila", "brandy", "vinous", "tart", "lacto", "honey", "clove", "bubblegum", "currant",
                          "grape", "tea", "blueberry", "blackberry", "cassis", "gooseberry", "loganberry", "nectar", "nectarine", "pomegranate",
                          "quince", "rasberry", "strawberry", "watermelon", "grapefruit", "lemongrass", "lime", "mandarin", "tangerine", "coconut",
                          "cream", "guava", "melon", "papaya", "rose", "cedar", "cognac", "hay", "tobacco", "mint", "sage", "thyme", "aniseed",
                          "cinnamon", "ginger", "pepper", "licorice", "candy", "cucumber", "garlic", "bouquet", "aromatic", "fragrant", "perfumed",
                          "faint", "musky", "subtle", "yeasty", "malty", "pungent", "burnt", "blossom", "hedgerow", "elderflower", "orchard"],
               "mouthfeel": ["soft", "delicate","acrid", "flat","mineral","spirit", "astringent", "body", "full-bodied", "medium-bodied", "light-bodied",
                             "unfolding", "aftertaste", "thick", "thin", "creamy", "smooth", "velvety", "oily", "tannic", "chalky", "drying", "slick",
                             "watery", "effervescent", "fizzy", "tingly", "prickly", "carbonated", "viscosity", "warming", "coating", "biting", "sharp",
                             "rusty"], "brewing": ["wheat", "hopping", "barrel", "conditioned", "fermentation", "wort", "mash", "sparging", "crashing",
                                                   "decoction", "strain", "adjuncts", "grains", "malt"],
               "technical": ["balance", "palate", "complexity", "depth", "nuanced", "refined", "structured", "profile", "round", "harmonious", "clean",
                             "crisp", "finish", "lingering", "evolving", "clarity", "purity", "dense", "robust", "powerful", "restrained", "vibrant",
                             "subdued", "heavy", "integrity", "layered", "benchmark", "classic", "signature", "finesse", "elegance", "exemplar",
                             "well-integrated", "flawless", "exceptional", "outstanding", "world-class", "traditional", "innovative", "unconventional",
                             "unique"],
                "appearance": ["hazy", "cloudy", "opaque", "translucent", "clear", "bright", "unfiltered", "filtered", "lacing", "foam", "frothy",
                               "rocky head", "stable head", "gold", "amber", "ruby", "copper", "dark", "black", "mahogany", "light", "straw",
                               "yellow", "chestnut", "tan", "off-white", "blonde", "bronze", "coal", "ebony", "inky", "milky", "muddy", "obsidian",
                               "sepia", "sunlight", "transparent"],
               "off_flavors": ["funky", "sherry","rotten", "sulphur", "egg", "goat", "sour", "tasteless", "inferior", "acidic", "oxidized", "piss",
                               "metallic", "cardboard", "stale", "sulfur", "skunky", "diacetyl", "phenolic", "acetaldehyde", "DMS", "cloying","cheesy",
                               "solvent", "overly bitter", "harsh", "vegetal", "cabbage", "rubber","soy","buttery", "musty", "moldy", "medicinal"]}

def get_exp_scores(data_path):
  
    with open(data_path, "rb") as f:
        temp_df = pkl.load(f)

    temp_df = pd.DataFrame(temp_df)
    for criterion in temp_df.keys():
        temp_df[criterion + '_score'] = temp_df['stems'].apply(lambda cell: len(list(set(cell) & set(temp_df[criterion]))))
    
    temp_df['expert_score'] = 0
    for criterion in expert_terms.keys():
        temp_df['expert_score'] += temp_df[criterion + '_score']
    
    return temp_df


def get_average_scores_time(df, user_threshold):
    # Copy the dataset
    merged_reviews = df.copy()

    # Normalize location names
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
        .query(f'num_users >= {user_threshold}')['location']
    )


    filtered_reviews = merged_reviews[
        merged_reviews['location'].isin(locations_with_sufficient_users)
    ]

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

def get_average_scores(df, user_threshold):
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
        .query(f'num_users >= {user_threshold}')['location']
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

def get_filtered_reviews(df, user_threshold):
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
        .query(f'num_users >= {user_threshold}')['location']
    )


    filtered_reviews = merged_reviews[
        merged_reviews['location'].isin(locations_with_sufficient_users)
    ]
    return filtered_reviews