from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
import string
# 
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    # 
    preprocessed_query = preprocess_text(query)
    # 
    for movie in movies:
        title = movie["title"]
        preprocessed_title = preprocess_text(title)
        if preprocessed_query in preprocessed_title:
            results.append(movie)
            if len(results) >= limit:
                break    
    return results

#
def preprocess_text(text: str) -> str:
    text = text.lower()
    # 
    text = text.translate(text.maketrans(text, text, string.punctuation))
    # 
    return text 
#  