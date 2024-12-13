import matplotlib.pyplot as plt
import pandas as pd
import os

def compute_occ(df):
    occ = {}
    for x in df:
        for term in x:
            if term in occ.keys():
                occ[term]+= 1
            else: 
                occ[term]= 1
    return pd.Series(occ)

def get_style_dfs(style, complete_beer, users, exp_categories):
    rev = complete_beer[complete_beer['style_x']==style]
    col_to_keep = ['user_id','stems'] + exp_categories
    rev = rev[col_to_keep]
    return rev, pd.merge(rev, users[['location', 'user_id']], on='user_id')

def plot_country_distrbution(complete_df, threshold=2000):
    loc_size = complete_df.groupby('location').size().sort_values()
    to_plot = loc_size[loc_size > threshold]
    fig  = plt.figure(figsize=(17,7))
    #plt.bar(to_plot.index, to_plot)
    to_plot.plot(kind='bar', logy=True)
    plt.xticks(rotation=90)
    plt.show()

def plot_country_exp_score(complete_df, sel_countries, style=''):
    loc_score = complete_df[complete_df['location'].isin(sel_countries)][['location', 'expertness_score']].groupby('location').mean()
    loc_score = loc_score.sort_values(by='expertness_score')
    plt.title(style + " Expertness_score")
    plt.bar(loc_score.index, loc_score.expertness_score)
    plt.xticks(rotation=45)
    plt.show()

def get_count_words(complete_df, sel_countries):
    count_words = pd.DataFrame()
    for c in sel_countries:
        count_words[c] = compute_occ(complete_df[complete_df['location']==c].stems)

    return count_words.fillna(0)

def plot_count_words(count_words, style=''):
    fig, axes = plt.subplots(3, 2, figsize=(12, 6)) 


    fig.suptitle(style + " Most frequent words per country", fontsize=16)

    for i, c in enumerate(count_words.columns):
        sel_c = count_words[c].sort_values(ascending =False).head(20)
        axes[i//2, i%2].bar(sel_c.index, sel_c, color='skyblue')
        plt.setp(axes[i//2, i%2].get_xticklabels(), rotation=45, ha='right')
        axes[i//2, i%2].set_title(c)
        
    plt.tight_layout()  
    plt.show()