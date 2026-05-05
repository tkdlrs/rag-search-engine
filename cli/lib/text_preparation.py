# 
import string
# 
from nltk.stem import PorterStemmer 
# 
from .search_utils import load_stopwords

# 
def preprocess_text(text: str) -> str:
    text = text.lower()
    # 
    text = text.translate(str.maketrans("", "", string.punctuation))
    # 
    return text 
# 
def tokenize_text(text: str) -> list[str]:
    tokens = text.split()
    tokens = list(filter(None, tokens))
    return tokens
# 
def remove_stop_words(tokens: list[str]) -> list[str]:
    stopwords = load_stopwords()
    return list(filter(lambda t: t not in stopwords, tokens))
# 
def stemification(token_list: list[str]) -> list[str]:
    stemmer = PorterStemmer()
    stems = []
    for token in token_list:
        stems.append(stemmer.stem(token))
    #  
    return stems
"""
""" 
def prep_text(text:str) -> list[str]:
    remove_punctuation = preprocess_text(text) 
    tokenize = tokenize_text(remove_punctuation)
    remove_stopwords = remove_stop_words(tokenize)
    stemify = stemification(remove_stopwords)
    return stemify
# 