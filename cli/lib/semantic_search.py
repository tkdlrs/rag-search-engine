# 
# 
from sentence_transformers import SentenceTransformer 

# Load the model (downloads auomatically the first time)
# model = SentenceTransformer('all-MiniLM-l6-v2')
# 
# print(f"Model loaded: {model}")
# print(f"Max sequence length: {model.max_seq_length}")
# 
# model.encode(text)

# 
class SemanticSearch:
    # 
    def __init__(self) -> None:
        self.model = SentenceTransformer('all-MiniLM-l6-v2')
        # 
    # 

# 
def verify_model():
    semanticSearch = SemanticSearch()
    print(f"Model loaded: {semanticSearch.model}")
    print(f"Max sequence length: {semanticSearch.model.max_seq_length}")
