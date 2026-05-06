
import os 
import pickle
# 
from collections import defaultdict, Counter
# 
from .text_preparation import prep_text 
# 
from .search_utils import (
    CACHE_DIR, 
    load_movies,
)
# 
class InvertedIndex:
    # 
    def __init__(self) -> None:
        self.index = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.term_frequencies: dict[int, Counter] = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        self.tf_path = os.path.join(CACHE_DIR, "term_frequencies.pkl")

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
        # 
        self.term_frequencies[doc_id] = Counter(tokens)
        # add each token to the index with the doc id
        for token in set(tokens):
            self.index[token].add(doc_id)
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
        return
    # 
    def get_tf(self, doc_id, term) -> int:
        doc_id = int(doc_id)
        term_token = prep_text(term)
        if len(term_token) > 1:
            raise Exception("invalid number of terms provided")
        # 
        return self.term_frequencies[doc_id][term_token[0]]
    # 

#      
def build_command() -> None:
     idx = InvertedIndex()
     idx.build()
     idx.save()     
# 
def tf_command(doc_id, term) -> None:
    idx = InvertedIndex()
    idx.load()
    result = idx.get_tf(doc_id, term)
    print(f"{result}")