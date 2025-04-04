import configparser
import os
from retainium.cli import process_cli
from retainium.knowledge import KnowledgeDB
from retainium.embeddings import EmbeddingHandler
from retainium.config import load_config

# Load configuration
config = load_config()

db_dir = config.get("database", "path", fallback="data/knowledge_db")
os.makedirs(db_dir, exist_ok=True)
knowledge_db = KnowledgeDB(db_dir)
embedding_handler = EmbeddingHandler()

if __name__ == "__main__":
    process_cli(knowledge_db, embedding_handler)
