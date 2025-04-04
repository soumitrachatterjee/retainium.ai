import os
from retainium.knowledge import KnowledgeDB
from retainium.embeddings import EmbeddingHandler
from retainium.cli import process_cli
from retainium.config import load_config

# Load configuration
config = load_config()
db_path = config.get("database", "path", fallback="data/knowledge_db")
embedding_model = config.get("embeddings", "model", fallback="all-MiniLM-L6-v2")

# Ensure database directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Initialize components
knowledge_db = KnowledgeDB(db_path)
embedding_handler = EmbeddingHandler(embedding_model)

# Process CLI commands
if __name__ == "__main__":
    process_cli(knowledge_db, embedding_handler)
