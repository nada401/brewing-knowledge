import matplotlib.pyplot as plt
import pandas as pd
import os
from wordcloud import WordCloud
from src.scripts.helpers import *

def compute_word_occ(df, word_occ):
    for x in df:
        if len(x)<1:
            continue
        for word in x:
            if word in word_occ.keys():
                word_occ[word]+= 1
            else: 
                word_occ[word]= 1
    return word_occ

def get_word_occ(rev_with_scores_ba, rev_with_scores_rb):
    word_occ = {}
    word_occ = compute_word_occ(rev_with_scores_rb.stems, word_occ)
    return compute_word_occ(rev_with_scores_ba.stems, word_occ)

def plot_word_cloud(data_path, word_occ):
    exp_dict = get_exp_dict_stems(data_path)

    for key in exp_dict:
        if exp_dict[key] in word_occ.keys():
            exp_dict[key] = word_occ[exp_dict[key]]
        else:
            exp_dict[key] = 0

    wordcloud = WordCloud(
        width=1600,  
        height=800,  
        background_color='white',
        colormap='viridis'
    ).generate_from_frequencies(exp_dict)

    plt.figure(figsize=(16, 8), dpi=300)  
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def plot_word_category_distribution(data_path, word_occ):
    exp_stems_per_cat = get_exp_stems(data_path)

    cat_distribution= {}
    for key, terms in exp_stems_per_cat.items():
        cat_distribution[key] = 0
        for term in terms:
            if term in word_occ.keys():
                cat_distribution[key] += word_occ[term]

    tot_occ = sum(cat_distribution.values())
    cat_dist_perc= {}
    for key in cat_distribution:
        cat_dist_perc[key] =  cat_distribution[key]/tot_occ
    
    plt.figure(figsize=(8, 8), dpi=200)
    plt.pie(
        cat_dist_perc.values(),
        labels=cat_dist_perc.keys(),
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    plt.title("Category Distribution", fontsize=16)
    plt.show()

