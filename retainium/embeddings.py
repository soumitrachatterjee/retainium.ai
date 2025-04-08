# retainium/embeddings.py

from sentence_transformers import SentenceTransformer
from retainium.diagnostics import Diagnostics

class EmbeddingHandler:
    def __init__(self, model_name: str):
        self.model_name = model_name
        Diagnostics.debug(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list:
        if not text.strip():
            Diagnostics.error("Attempted to embed empty text.")
            return []
        return self.model.encode(text, convert_to_tensor=False).tolist()
