import chromadb
import os
import uuid
from typing import List

class KnowledgeDB:
    #def __init__(self, db_path: str, collection_name: str = "knowledge"):
    def __init__(self, db_path="data/knowledge_db", collection_name="retainium_knowledge"):
        os.makedirs(db_path, exist_ok=True)  # Ensure the directory exists
        self.client = chromadb.PersistentClient(path=db_path)
        #self.collection = self.client.get_or_create_collection(name=collection_name)
        self.collection = self.client.get_or_create_collection(name=collection_name)  # Valid collection name

    def add_entry(self, text: str, embedding: List[float]):
        """Adds a new entry to the knowledge database with embedding."""
        if not isinstance(embedding, list) or not all(isinstance(i, float) for i in embedding):
            raise ValueError("Embedding must be a list of floats.")

        doc_id = str(uuid.uuid4())  # Generate a unique ID

        self.collection.add(
            documents=[text],
            metadatas=[{"source": "retainium"}],  # Ensuring metadata is not empty
            embeddings=[embedding],  # Properly passing embeddings
            ids=[doc_id]
        )
        print(f"Entry added with ID: {doc_id}")
        return doc_id

    def query(self, text: str, embedding: List[float], top_k: int = 5):
        """Retrieves the most relevant entries based on embedding similarity."""
        if not isinstance(embedding, list) or not all(isinstance(i, float) for i in embedding):
            raise ValueError("Embedding must be a list of floats.")

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        
        retrieved_docs = results.get("documents", [[]])[0]  # Extract documents from result
        return retrieved_docs
