from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingHandler:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding model."""
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a given text."""
        if not text or not isinstance(text, str):
            raise ValueError("Text input must be a non-empty string.")

        embedding = self.model.encode([text])[0]

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
            raise ValueError("Embedding must be a list of floats, but received an invalid format.")

        return embedding
