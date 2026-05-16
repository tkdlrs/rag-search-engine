import numpy as np 
import os 
# 
from sentence_transformers import SentenceTransformer 
# 
from .search_utils import (
    CACHE_DIR,
    load_movies,

)
# 
class SemanticSearch:
    def __init__(self, model_name="all-MiniLM-l6-v2") -> None:
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.documents = None
        self.document_map = {}

        self.movie_embeddings_path = os.path.join(CACHE_DIR, "movie_embeddings.npy")

        #
    def generate_embedding(self, text:str) -> str:
        if not text or not text.strip():
            raise ValueError("cannot generate embedding for empty text")
        # 
        embedding = self.model.encode([text])
        return embedding[0]
    # 
    def build_embeddings(self, documents):
        self.documents = documents
        # 
        movie_list = []
        # 
        for doc in documents:
            id = doc["id"]
            self.document_map[id] = doc
            # 
            str_representation = f"{doc['title']}: {doc['description']}"
            movie_list.append(str_representation)
            # 
        embeddings = self.model.encode(movie_list, show_progress_bar=True)
        self.embeddings = embeddings
        # 
        with open(self.movie_embeddings_path, "wb") as f:
            np.save(f, embeddings)
        # 
        return self.embeddings
    # 
    def load_or_create_embeddings(self, documents):
        self.documents = documents
        # 
        for doc in documents:
            id = doc["id"]
            self.document_map[id] = doc 
            # 
        # 
        if os.path.exists(self.movie_embeddings_path):
            with open(self.movie_embeddings_path, "rb") as f:
                self.embeddings = np.load(f)
            if len(self.embeddings) == len(documents):
                return self.embeddings
            # 
        else:
            self.build_embeddings(documents)
        # 

    # 
# 
def verify_model():
    search_instance = SemanticSearch()
    print(f"Model loaded: {search_instance.model}")
    print(f"Max sequence length: {search_instance.model.max_seq_length}")
# 
def embed_text(text:str):
    search_instance = SemanticSearch()
    embedding = search_instance.generate_embedding(text)
    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")
# 
def verify_embeddings():
    search_instance = SemanticSearch()
    documents = load_movies()
    embeddings = search_instance.load_or_create_embeddings(documents)
    print(f"Number of docs: {len(documents)}")
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")
# 
# 
