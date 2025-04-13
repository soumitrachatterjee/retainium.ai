from sentence_transformers import SentenceTransformer
from retainium.diagnostics import Diagnostics

class EmbeddingHandler:
    def __init__(self, model_name: str):
        self.model_name = model_name
        Diagnostics.note(f"loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list:
        if not text.strip():
            Diagnostics.error("attempted to embed empty text.")
            return []

        embedding = self.model.encode(text, convert_to_tensor=False).tolist()
        return embedding

