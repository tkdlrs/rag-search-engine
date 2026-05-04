import string
# 
from nltk.stem import PorterStemmer 
# 
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords
# 
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    # 
    preprocessed_query = preprocess_text(query)
    query_tokens = tokenize_text(preprocessed_query)
    query_tokens = remove_stop_words(query_tokens)
    query_tokens = stemification(query_tokens)
    # Matching logic 
    for movie in movies:
        title = movie["title"]
        preprocessed_title = preprocess_text(title)
        title_tokens = tokenize_text(preprocessed_title)
        title_tokens = remove_stop_words(title_tokens)
        title_tokens = stemification(title_tokens)
        #
        if has_matching_token(query_tokens, title_tokens):
            results.append(movie)
            if len(results) >= limit:
                break    
    # 
    return results
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
def has_matching_token(query_tokens: list[str], search_tokens: list[str]) -> bool: 
    for q_token in query_tokens:
        for s_token in search_tokens:
            if q_token in s_token:
                return True
    # 
    return False
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
# 

