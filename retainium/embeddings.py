from sentence_transformers import SentenceTransformer

class EmbeddingHandler:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text: str):
        """Generate an embedding vector for a given text."""
        return self.model.encode(text).tolist()
