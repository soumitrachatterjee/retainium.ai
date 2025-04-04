from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingHandler:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text: str):
        """Generate an embedding vector for a given text."""
        return self.model.encode(text).tolist()

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode([text])[0]  # Example for sentence-transformers

        # Ensure conversion to list of floats
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
    
        if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
            raise ValueError("Embedding must be a list of floats.")
    
        return embedding
