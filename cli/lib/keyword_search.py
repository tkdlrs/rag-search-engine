from .search_utils import DEFAULT_SEARCH_LIMIT, load_movies
# 
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies = load_movies()
    results = []
    # 
    for movie in movies:
        title = movie["title"]
        if query in title:
            results.append(movie)
            if len(results) >= limit:
                break    
    return results
