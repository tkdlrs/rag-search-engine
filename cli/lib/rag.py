import os 
from typing import TypedDict 
# 
from dotenv import load_dotenv
from google import genai
# 
from .hybrid_search import HybridSearch 
from .search_utils import (
    load_movies, 
)
from .semantic_search import SemanticSearch
# 
# 
class QueryEvaluationResult(TypedDict):
    precision: float 
    recall: float 
    f1_score: float 
    retrieved: list[str]
    relevant: list[str]
# 
# 
class EvaluationSummary(TypedDict):
    test_cases_count: int 
    limit: int
    results: dict[str, QueryEvaluationResult]
# 
# 
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable not set")
# 
client = genai.Client(api_key=api_key)
model = "gemma-4-31b-it"
#

def rag_command(query: str):
    movies = load_movies()
    searcher = HybridSearch(movies)
    # 
    docs = searcher.rrf_search(query, limit=5)
    # 
    prompt = f"""You are a RAG agent for Hoopla, a movie streaming service.
    Your task is to provide a natural-language answer to the user's query based on documents retrieved during search.
    Provide a comprehensive answer that addresses the user's query.

    Query: {query}

    Documents:
    {docs}

    Answer:"""

    response = client.models.generate_content(model=model, contents=prompt)
    rag_response = (response.text or "").strip()

    # 
    return {
        "query": query, 
        "results": docs,
        "response": rag_response
    }