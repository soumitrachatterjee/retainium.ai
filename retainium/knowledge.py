# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Compute project root relative to this script
# (protect against symlinks using realpath())
import os
root = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

# Import required modules
import hashlib
import base64
from typing import List
from dataclasses import dataclass, asdict
import chromadb
from chromadb.config import Settings
from retainium.diagnostics import Diagnostics

# The knowledge database collection name
# (changing this can cause loss of existing knowledge)
COLLECTION_NAME = "retainium_knowledge"

# Compute a hash from the text to serve as the unique id and to aid deduplication
def compute_text_uuid(text: str) -> str:
    sha256_digest = hashlib.sha256(text.strip().encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256_digest).decode("utf-8").rstrip("=")

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
    def add_entry(self, text: str, source: str, embedding_handler, llm_handler) -> None:
        # Guard against empty text
        if not text:
            Diagnostics.warning("request to add empty entry ignored")
            return

        # Auto generate tags for the entry
        tags = llm_handler.auto_tags(text)
        Diagnostics.debug(f"auto generated tags: {tags}")

        #date = datetime.now().strftime('%Y-%m-%d') # TODO 

        # Generate the knowledge entry and the corresponding embedding
        entry = KnowledgeEntry(
                                id=compute_text_uuid(text), 
                                text=text, 
                                source=source, 
                                tags=tags
                              )
        embedding_vector = embedding_handler.embed(text)

        # Warn about duplicate entries only in debug mode
        if Diagnostics.is_debug_enabled():
            existing = self.collection.get(ids=[entry.id])
            if existing['ids']:  # Already present
                Diagnostics.warning(f"duplicate entry skipped: {entry.id[:16]}")
                return

        # Add to the vector database
        # (ignore duplicate entries silently in non-debug mode)
        self.collection.add(
                            ids=[entry.id],
                            documents=[entry.text],
                            embeddings=[embedding_vector],
                            metadatas=[entry.to_metadata()],
        )
        Diagnostics.note(f"entry added successfully: {entry.id[:16]}")

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

    # Return a list of all existing knowledge entries
    def export_all(self) -> List[dict]:
        return [entry.to_dict() for entry in self.list_entries()]

    # Delete the existing collection and recreate using stored entries
    # Return a list of all existing entries
    def reinitialize_collection(self, knowledge_db) -> List[KnowledgeEntry]:
        # Fetch the list of all existing entries
        entries = knowledge_db.list_entries()

        # Reinitialize the collection
        self.client.delete_collection(COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)

        # Return the list of entries to be added back
        return entries

