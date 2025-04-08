import os
import json
import uuid
from datetime import datetime
from retainium.diagnostics import Diagnostics
import chromadb

class KnowledgeDB:
    def __init__(self, config):
        # Accepts either config object or direct path string
        if isinstance(config, str):
            self.db_path = config
        else:
            self.db_path = config.get("database", "path", fallback="data/knowledge_db")

        os.makedirs(self.db_path, exist_ok=True)

        # Initialize ChromaDB client and collection
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name="knowledge")

    def normalize_entry(self, entry: dict) -> dict:
        """Ensure the entry follows the expected format."""
        if not isinstance(entry, dict):
            raise ValueError("Each entry must be a dictionary.")

        # Support nested document field
        if "document" in entry and isinstance(entry["document"], dict):
            doc = entry["document"]
            entry["text"] = doc.get("text", entry.get("text", ""))
            entry.pop("document")

        # Ensure required fields
        required_fields = ["id", "text", "embedding"]
        for field in required_fields:
            if field not in entry or not entry[field]:
                raise ValueError(f"Missing required field in knowledge entry: {field}")

        # Set default optional fields
        entry.setdefault("tags", [])
        entry.setdefault("source", "")
        entry.setdefault("timestamp", datetime.now().isoformat())

        return entry

    def add_entry(self, text: str, embedding: list[float], tags: list[str] = None, source: str = None):
        entry_id = str(uuid.uuid4())
        entry = {
            "id": entry_id,
            "text": text,
            "embedding": embedding,
            "tags": tags or [],
            "source": source or "",
            "timestamp": datetime.now().isoformat()
        }

        validated = self.normalize_entry(entry)

        file_path = os.path.join(self.db_path, f"{entry_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(validated, f, ensure_ascii=False, indent=2)

        Diagnostics.debug(f"Added entry with ID {entry_id}")

    def list_entries(self) -> list:
        entries = []
        for filename in os.listdir(self.db_path):
            if filename.endswith(".json"):
                file_path = os.path.join(self.db_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        entry = json.load(f)
                        if isinstance(entry, list):
                            Diagnostics.warning(f"Skipping list-based legacy file: {filename}")
                            continue
                        entry = self.normalize_entry(entry)
                        entries.append(entry)
                    except Exception as e:
                        Diagnostics.warning(f"Failed to load entry from {filename}: {e}")
        return entries

    def get_all_embeddings(self) -> list[tuple[str, list[float]]]:
        """Return list of (id, embedding) tuples for similarity search."""
        result = []
        for entry in self.list_entries():
            result.append((entry["id"], entry["embedding"]))
        return result

    def get_entry_by_id(self, entry_id: str) -> dict | None:
        file_path = os.path.join(self.db_path, f"{entry_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                entry = json.load(f)
                return self.normalize_entry(entry)
            except Exception as e:
                Diagnostics.warning(f"Failed to load entry {entry_id}: {e}")
                return None

    def query(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        """Query the ChromaDB collection using a vector and return top matches."""
        if not self.collection:
            return []
    
        try:
            results = self.collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
                include=["documents", "distances", "metadatas"]
            )
        except Exception as e:
            Diagnostics.warning(f"Failed to query vector DB: {e}")
            return []
    
        # Post-process the results
        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
    
        matches = []
        for doc, dist, meta, doc_id in zip(documents, distances, metadatas, ids):
            match = {
                "id": doc_id,
                "document": doc,
                "tags": meta,
                "score": 1.0 - dist  # Chroma returns L2 distance; convert to similarity
            }
            matches.append(match)
    
        return matches

