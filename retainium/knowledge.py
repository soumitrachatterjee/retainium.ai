import chromadb
import uuid

class KnowledgeDB:
    def __init__(self, collection_name="retainium_knowledge"):
        self.client = chromadb.PersistentClient(path="data/knowledge_db")  # Ensure persistence
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_entry(self, text, embedding):
        """Adds a new entry to the knowledge database with embedding."""
        if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
            raise ValueError("Embedding must be a list of floats.")
        
        doc_id = str(uuid.uuid4())  # Generate a unique ID
        self.collection.add(
            documents=[text], 
            metadatas=[{}],  # Empty metadata for now
            embeddings=[embedding],  # Properly passing embeddings
            ids=[doc_id]
        )
        print(f"Entry added with ID: {doc_id}")

    def query_entry(self, query_text, embedding, top_k=5):
        """Retrieves the most relevant entries based on embedding similarity."""
        if not isinstance(embedding, list) or not all(isinstance(x, float) for x in embedding):
            raise ValueError("Embedding must be a list of floats.")
        
        results = self.collection.query(
            query_embeddings=[embedding], 
            n_results=top_k
        )
        
        return results["documents"][0] if "documents" in results else []
