# Compute project root relative to this script
# (protect against symlinks using realpath())
import os
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Import required modules
import uuid
from typing import List
from dataclasses import dataclass, asdict
import chromadb
from chromadb.config import Settings
from retainium.diagnostics import Diagnostics

# The knowledge database collection name
# (changing this can cause loss of existing knowledge)
COLLECTION_NAME = "retainium_knowledge"

# The record for each knowledge entry
@dataclass
class KnowledgeEntry:
    id: str
    text: str
    source: str
    tags: List[str]

    def to_metadata(self) -> dict:
        return {
            "source": self.source,
            "tags": ",".join(self.tags),
        }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "source": self.source,
            "tags": self.tags,
        }

# The knowledge database class
class KnowledgeDB:
    def __init__(self, persist_directory: str = os.path.join(root, "data", "knowledge_db")):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True) # Ensure the directory exists
        Diagnostics.note(f"knowledge database initialized at {self.persist_directory}")

        # Setup ChromaDB as the persistent knowledge database
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
        Diagnostics.note(f"using ChromaDB client collection \"{self.collection.name}\"")

    # Add the knowledge to the database along with the corresponding embedding
    def add_entry(self, entry: KnowledgeEntry, embedding: List[float]) -> None:
        self.collection.add(
            ids=[entry.id],
            documents=[entry.text],
            embeddings=[embedding],
            metadatas=[entry.to_metadata()],
        )
        Diagnostics.note(f"entry added successfully: {entry.id}")

    # Fetch and list all entries from the database
    def list_entries(self) -> List[KnowledgeEntry]:
        results = self.collection.get()
        entries = []
        for i in range(len(results["ids"])):
            metadata = results["metadatas"][i]
            tags = metadata.get("tags", "").split(",") if metadata.get("tags") else []
            entries.append(
                KnowledgeEntry(
                    id=results["ids"][i],
                    text=results["documents"][i],
                    source=metadata.get("source", "unknown"),
                    tags=tags,
                )
            )
        return entries

    # Query the knowledge database for the specific embedding
    def query_entry(self, embedding: List[float], top_k: int = 5) -> List[KnowledgeEntry]:
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        entries = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            tags = metadata.get("tags", "").split(",") if metadata.get("tags") else []
            entries.append(
                KnowledgeEntry(
                    id=results["ids"][0][i],
                    text=results["documents"][0][i],
                    source=metadata.get("source", "unknown"),
                    tags=tags,
                )
            )
        return entries

    def export_all(self) -> List[dict]:
        return [entry.to_dict() for entry in self.list_entries()]

    def rebuild_index(self, entries: List[KnowledgeEntry], embeddings: List[List[float]]):
        self.client.delete_collection("knowledge")
        self.collection = self.client.get_or_create_collection("knowledge")
        for entry, embedding in zip(entries, embeddings):
            self.add_entry(entry, embedding)

# Alias for consistency across the codebase
KnowledgeDatabase = KnowledgeDB
