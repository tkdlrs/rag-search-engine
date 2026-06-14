import os
from typing import Any
# 
from PIL import Image
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
# 
from lib.search_utils import Movie, load_movies
from lib.semantic_search import cosine_similarity
#
# 
class MultimodalSearch:
    def __init__(
            self, documents: list[object] | None = None, model_name: str = "clip-ViT-B-32"
    ) -> None:
        if documents is None:
            documents = []
        self.documents = documents
        self.texts: list[str] = []
        for doc in documents:
            self.texts.append(f"{doc['title']}: {doc['description']}")
        # 
        self.model = SentenceTransformer(model_name)
        self.text_embeddings = self.model.encode(self.texts, show_progress_bar=True)
    # 
    def embed_image(self, image_path: str) -> NDArray[Any]:
         if not os.path.exists(image_path):
             raise FileNotFoundError(f"Image file not found: {image_path}")
         image = Image.open(image_path)
         image_embedding = self.model.encode([image]) # type: ignore[arg-type]
         return image_embedding[0]
    # 
    def search_with_image(self, image_path: str) -> list[dict]:
        image_embedding = self.embed_image(image_path)
        # 
        similarities: list[tuple[float, Movie]] = []
        for i, text_embedding in enumerate(self.text_embeddings):
            similarity = cosine_similarity(text_embedding, image_embedding )
            similarities.append((similarity, self.documents[i]))
        #          
        similarities.sort(key=lambda x: x[0], reverse=True)
        # 
        results = []
        for i, similarity in enumerate(similarities):
            if i >= 5: break
            # 
            results.append({  
                "id": similarity[1]["id"],
                "title": similarity[1]["title"],
                "description": similarity[1]["description"],
                "similarity_score": similarity[0],
            })
        # 
        return results
#         
# 
def verify_image_embedding(image_path: str) -> None:
    searcher = MultimodalSearch()
    embedding = searcher.embed_image(image_path)
    print(f"Embedding shape: {embedding.shape[0]} dimensions")
# 
# 
def image_search_command(image_path: str) -> list[object]:
    movies = load_movies()
    searcher = MultimodalSearch(movies)
    return searcher.search_with_image(image_path)
# 
# 
