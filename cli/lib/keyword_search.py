# 
from .search_utils import DEFAULT_SEARCH_LIMIT 
# 
from .inverted_index import InvertedIndex
from .text_preparation import prep_text
# 
def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    # movies = load_movies()
    idx = InvertedIndex()
    try:
        idx.load()
    except FileExistsError:
        print(f"file not found")
    # 
    results = []
    # 
    query_tokens = prep_text(query)
    # Matching logic 
    for qt in query_tokens:
        if len(results) >= limit:
            break
        # 
        qts_matches = idx.get_documents(qt)
        if len(qts_matches):
            for match in qts_matches:
                results.append(idx.docmap[match])
                if len(results) >= limit:
                    return results 
    # 
    return results
#
def has_matching_token(query_tokens: list[str], search_tokens: list[str]) -> bool: 
    for q_token in query_tokens:
        for s_token in search_tokens:
            if q_token in s_token:
                return True
    # 
    return False
# 
