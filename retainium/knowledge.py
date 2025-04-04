import chromadb
import os
import uuid
from typing import List

class KnowledgeDB:
    def __init__(self, db_path="data/knowledge_db", collection_name="retainium_knowledge"):
        os.makedirs(db_path, exist_ok=True)  # Ensure the directory exists
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

        if self.collection is None:
            raise RuntimeError("Failed to create or retrieve the collection.")

    def list_entries(self):
        """Lists all stored knowledge entries."""
        data = self.collection.get()
        if "ids" not in data or "documents" not in data:
            return []

        return [{"id": entry_id, "document": doc} for entry_id, doc in zip(data["ids"], data["documents"])]

    def add_entry(self, text: str, embedding: List[float]):
        """Adds a new entry to the knowledge database with embedding."""
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string.")

        if not isinstance(embedding, list) or not embedding or not all(isinstance(i, float) for i in embedding):
            raise ValueError("Embedding must be a non-empty list of floats.")

        doc_id = str(uuid.uuid4())

        self.collection.add(
            documents=[text],
            metadatas=[{"source": "retainium"}],
            embeddings=[embedding],
            ids=[doc_id]
        )

        print(f"Entry added with ID: {doc_id}")
        return doc_id

    def query(self, embedding: List[float], top_k: int = 5):
        """Retrieves the most relevant entries based on embedding similarity."""
        if not isinstance(embedding, list) or not all(isinstance(i, float) for i in embedding):
            raise ValueError("Embedding must be a list of floats.")
    
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
    
        retrieved_docs = results.get("documents", [[]])[0]  # Extract documents from result
        return retrieved_docs
