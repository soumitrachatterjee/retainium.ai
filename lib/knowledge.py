import chromadb

class KnowledgeDB:
    def __init__(self, db_path: str):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="knowledge")

    def add_entry(self, text: str, metadata: dict):
        """Add a new entry to the knowledge database."""
        doc_id = str(hash(text))
        self.collection.add(documents=[text], metadatas=[metadata], ids=[doc_id])

    def query(self, text: str, n_results: int = 5):
        """Retrieve relevant knowledge entries based on similarity search."""
        results = self.collection.query(query_texts=[text], n_results=n_results)
        return results
