
import os 
import pickle
import math
# 
from collections import defaultdict, Counter
# 
from .text_preparation import prep_text 
# 
from .search_utils import (
    BM25_K1,
    BM25_B,
    DEFAULT_SEARCH_LIMIT,
    CACHE_DIR, 
    load_movies,
    format_search_result,
)
#  
class InvertedIndex:
    # 
    def __init__(self) -> None:
        self.index = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        self.tf_path = os.path.join(CACHE_DIR, "term_frequencies.pkl")
        self.term_frequencies = defaultdict(Counter)
        self.doc_lengths: dict[int, int] = {}
        self.doc_lengths_path = os.path.join(CACHE_DIR, "doc_lengths.pkl")

    # 
    def build(self) -> None:
        # get movies
        movies = load_movies()
        # iterate over all movies and add to both index and docmap
        for m in movies:
            doc_id = m["id"]
            doc_text = f"{m['title']} {m['description']}"
            self.docmap[doc_id] = m
            self.__add_document(doc_id, doc_text)        
    # 
    def save(self) -> None:
        os.makedirs(CACHE_DIR, exist_ok=True)
        # save the index to 'cache/index.pkl'
        try:
            with open(self.index_path, 'wb' ) as f:
                pickle.dump(self.index, f)
        except Exception as e:
            print(f"An error occurred while pickling index: {e}")
        # save the docmap to 'cache/docmap.pkl'
        try: 
            with open(self.docmap_path, "wb") as f:
                pickle.dump(self.docmap, f)
        except Exception as e:
            print(f"An error occurred while pickling docmap: {e}")
        # save the term_frequencies to 'cache/term_frequencies.pkl'
        try:
            with open(self.tf_path, "wb") as f:
                pickle.dump(self.term_frequencies, f)
        except Exception as e:
            print(f"An error occurred while pickling term_frequencies: {e}")
        # save the doc_lengths to 'cache/doc_lengths.pkl'
        try:
            with open(self.doc_lengths_path, "wb") as f:
                pickle.dump(self.doc_lengths, f)
        except Exception as e:
            print(f"An error occurred while pickling doc_lengths: {e}")
        # 
        return
    # 
    def get_documents(self, term: str) -> list[int]:
        # lowercase term
        term = term.lower()
        # get set of doc ids for token 
        doc_ids = self.index.get(term, set())
        # sort ascending order
        return sorted(list(doc_ids))
    # 
    def __add_document(self, doc_id, text) -> None:
        # Tokenize input text
        tokens = prep_text(text)
        # add each token to the index with the doc id
        for token in set(tokens):
            self.index[token].add(doc_id)
        # 
        self.term_frequencies[doc_id].update(tokens)
        self.doc_lengths[doc_id] = len(tokens)
        # 
    # 
    def load(self) -> None:
        # Get index
        try:
            with open(self.index_path, "rb") as iFile:
                self.index = pickle.load(iFile)
        except Exception as e:
            print(f"An error occurred while loading the pickled index_path: {e}")
        # Get Docmap
        try:
            with open(self.docmap_path, "rb") as dFile:
                self.docmap = pickle.load(dFile)
        except Exception as e: 
            print(f"An error occurred while loading the pickled dockmap_path: {e}")
        # Get term_frequencies
        try:
            with open(self.tf_path, "rb") as tFile:
                self.term_frequencies = pickle.load(tFile)
        except Exception as e:
            print(f"An error occurred while loading the picked term_frequencies: {e}")
        # 
        try:
            with open(self.doc_lengths_path, "rb") as dlFile:
                self.doc_lengths = pickle.load(dlFile)
        except Exception as e:
            print(f"An error occurred while loading the picked doc_lengths: {e}")
        # 
        return
    # 
    def get_tf(self, doc_id: int, term: str) -> int:
        tokens = prep_text(term)
        if len(tokens) != 1:
            raise ValueError("term must be a single token")
        token = tokens[0]
        # 
        return self.term_frequencies[doc_id][token]
    # 
    def get_idf(self, term:str) -> float:
        tokens = prep_text(term)
        if len(tokens) != 1:
            raise ValueError("term must be a single token")
        token = tokens[0]
        doc_count = len(self.docmap)
        term_doc_count = len(self.index[token])
        return math.log((doc_count + 1) / (term_doc_count + 1))
    # 
    def get_tf_idf(self, doc_id: int, term: str) -> float:
        tf = self.get_tf(doc_id, term)
        idf = self.get_idf(term)
        return tf * idf
    # 
    def get_bm25_idf(self, term: str) -> float:
        tokens = prep_text(term)
        if len(tokens) != 1:
            raise ValueError("term must be a single token")
        token = tokens[0]
        doc_count = len(self.docmap)
        term_doc_count = len(self.index[token])
        return math.log((doc_count - term_doc_count + 0.5) / (term_doc_count + 0.5) + 1)
    # 
    def get_bm25_tf(self, doc_id: int, term: str, k1: float = BM25_K1, b: float = BM25_B) -> float:
        tf = self.get_tf(doc_id, term)
        # 
        doc_length = self.doc_lengths.get(doc_id, 0)
        avg_doc_length = self.__get_avg_doc_length()
        # 
        if avg_doc_length > 0:
            length_norm = 1 - b + b * (doc_length / avg_doc_length)
        else:
            length_norm = 1
        # 
        tf_component = (tf * (k1 + 1)) / (tf + k1 * length_norm)        
        # 
        return tf_component
    # 
    def __get_avg_doc_length(self) -> float:
        if not self.doc_lengths or len(self.doc_lengths) == 0:
            return 0.0
        # 
        total_length = 0
        for length in self.doc_lengths.values():
            total_length += length
        # 
        return total_length / len(self.doc_lengths)
    #
    def bm25(self, doc_id: int, term: str) -> float:
        bm25_tf_component = self.get_bm25_tf(doc_id, term)
        bm25_idf_component = self.get_bm25_idf(term)
        return bm25_tf_component * bm25_idf_component
    #
    def bm25_search(self, query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
        # tokenize input 
        query_tokens = prep_text(query)
        # maps document IDs to total BM25 scores
        scores = {}
        for doc_id in self.docmap:
            score = 0.0
            for token in query_tokens:
                score += self.bm25(doc_id, token)
            scores[doc_id] = score
            # 
        # 
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        # 
        results = []
        for doc_id, score in sorted_docs[:limit]:
            doc = self.docmap[doc_id]
            formatted_result = format_search_result(
                doc_id = doc["id"], 
                title = doc["title"], 
                document = doc["description"], 
                score = score,
            )
            results.append(formatted_result)
        # 
        return results
    # 
    # 
# 
#      
def build_command() -> None:
     idx = InvertedIndex()
     idx.build()
     idx.save()     
# 
def tf_command(doc_id:int, term:str) -> int:
    idx = InvertedIndex()
    idx.load()
    return idx.get_tf(doc_id, term)
# 
def idf_command(term: str) -> float:
    idx = InvertedIndex()
    idx.load()
    return idx.get_idf(term)
# 
def tfidf_command(doc_id: int, term: str) -> float:
    idx = InvertedIndex()
    idx.load()
    return idx.get_tf_idf(doc_id, term)
# 
def bm25_idf_command(term: str) -> float:
    idx = InvertedIndex()
    idx.load()
    return idx.get_bm25_idf(term)
# 
def bm25_tf_command(doc_id: int, term: str, k1: float = BM25_K1, b: float = BM25_B) -> float:
    idx = InvertedIndex()
    idx.load()
    return idx.get_bm25_tf(doc_id, term, k1, b)
# 
def bm25search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    idx = InvertedIndex()
    idx.load()
    return idx.bm25_search(query, limit)
# 
# 

    