
import os 
import pickle
# 
from collections import defaultdict
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
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
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
        # 
    # 
    def get_documents(self, term: str) -> list[int]:
        # lowercase term
        term = term.lower()
        # get set of doc ids for token 
        doc_ids = self.index.get(term, set())
        # sort ascending order
        return sorted(list(doc_ids))
    # 
    def __add_document(self, doc_id, text):
        # Tokenize input text
        tokens = prep_text(text)
        # add each token to the index with the doc id
        for token in set(tokens):
            self.index[token].add(doc_id)
    # 
    def load(self) -> None:
        # Get index
        try:
            with open(self.index_path, 'rb') as iFile:
                self.index = pickle.load(iFile)
        except Exception as e:
            print(f"An error occurred while loading the pickled index_path: {e}")
        # Get Docmap
        try:
            with open(self.docmap_path, 'rb') as dFile:
                self.docmap = pickle.load(dFile)
        except Exception as e: 
            print(f"An error occurred while loading the pickled dockmap_path: {e}")
        # 
        return
#      
def build_command() -> None:
     idx = InvertedIndex()
     idx.build()
     idx.save()     
# 