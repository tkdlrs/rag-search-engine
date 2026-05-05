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
    query_tokens = prep_text(query)
    seen, results = set(), []
    # Matching logic 
    for query_token in query_tokens:
        matching_doc_ids = idx.get_documents(query_token)
        # 
        if len(matching_doc_ids):
            for doc_id in matching_doc_ids:
                if doc_id in seen:
                    continue
                seen.add(doc_id)
                doc = idx.docmap[doc_id]
                results.append(doc)
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
