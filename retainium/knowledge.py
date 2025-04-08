# retainium/knowledge.py

import os
import uuid
from typing import List
from dataclasses import dataclass, asdict
import chromadb
from chromadb.config import Settings

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

class KnowledgeDB:
    def __init__(self, persist_directory: str = "data/knowledge_db"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        print(f"[DEBUG] Knowledge DB initialized at {self.persist_directory}")

        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection("knowledge")

    def add_entry(self, entry: KnowledgeEntry, embedding: List[float]) -> None:
        self.collection.add(
            ids=[entry.id],
            documents=[entry.text],
            embeddings=[embedding],
            metadatas=[entry.to_metadata()],
        )

    def get_all_entries(self) -> List[KnowledgeEntry]:
        results = self.collection.get()
        entries = []
        for i in range(len(results["ids"])):
            metadata = results["metadatas"][i]
            tags_list = metadata.get("tags", "").split(",") if metadata.get("tags") else []
            entries.append(KnowledgeEntry(
                id=results["ids"][i],
                text=results["documents"][i],
                source=metadata.get("source", "unknown"),
                tags=tags_list,
            ))
        return entries

    def query_similar(self, embedding: List[float], top_k: int = 3) -> List[KnowledgeEntry]:
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        entries = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            tags_list = metadata.get("tags", "").split(",") if metadata.get("tags") else []
            entries.append(KnowledgeEntry(
                id=results["ids"][0][i],
                text=results["documents"][0][i],
                source=metadata.get("source", "unknown"),
                tags=tags_list,
            ))
        return entries

    def export_all(self) -> List[dict]:
        return [entry.to_dict() for entry in self.get_all_entries()]

    def rebuild_index(self, entries: List[KnowledgeEntry], embeddings: List[List[float]]):
        self.client.delete_collection("knowledge")
        self.collection = self.client.get_or_create_collection("knowledge")
        for entry, embedding in zip(entries, embeddings):
            self.add_entry(entry, embedding)

# Alias for consistency across the codebase
KnowledgeDatabase = KnowledgeDB
