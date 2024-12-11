import json
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

def get_exp_stems_set(expert_terms):
    exp_stem_set = []
    for category, terms in expert_terms.items():
        tokens = [word_tokenize(term.lower()) for term in terms]
    
        stemmer = SnowballStemmer('english')
        stemmed_tokens = [stemmer.stem(word[0]) for word in tokens]
        exp_stem_set = exp_stem_set + stemmed_tokens
    
    return set(exp_stem_set)

def get_exp_terms(data_path):
    with open(os.path.join(data_path, 'expert_terms.json'), 'r') as f:
        expert_terms = json.load(f)
    return expert_terms

def get_exp_categories(data_path):
    return list(get_exp_terms(data_path).keys())

def get_exp_stems(data_path):
    expert_terms = get_exp_terms(data_path)
    expert_terms_stemmed = {}
    for category, terms in expert_terms.items():
        tokens = [word_tokenize(term.lower()) for term in terms]
        
        stemmer = SnowballStemmer('english')
        stemmed_tokens = [stemmer.stem(word[0]) for word in tokens]
        expert_terms_stemmed[category] =  stemmed_tokens
    return expert_terms_stemmed
