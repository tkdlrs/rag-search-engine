import string
# 
from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
# 
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    # 
    preprocessed_query = preprocess_text(query)
    tokenized_query = tokenize(preprocessed_query)
    # 
    for movie in movies:
        title = movie["title"]
        preprocessed_title = preprocess_text(title)
        tokenized_title = tokenize(preprocessed_title)
        # if preprocessed_query in preprocessed_title:
        if token_match(tokenized_query, tokenized_title):
            results.append(movie)
            if len(results) >= limit:
                break    
    return results

#
def preprocess_text(text: str) -> str:
    text = text.lower()
    # 
    text = text.translate(str.maketrans("", "", string.punctuation))
    # 
    return text 
# 
def tokenize(text: str) -> list[str]:
    tokens = text.split(" ")
    tokens = list(filter(None, tokens))
    return tokens
    
# 
def token_match(query_tokens: list[str], search_tokens: list[str]) -> bool: 
    for q_token in query_tokens:
        for s_token in search_tokens:
            if q_token in s_token:
                return True
    # 
    return False

# 