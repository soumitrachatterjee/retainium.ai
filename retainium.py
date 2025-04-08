import os
from configparser import ConfigParser

from retainium.cli import process_cli
from retainium.knowledge import KnowledgeDatabase
from retainium.embeddings import EmbeddingHandler
from retainium.llm import LLMHandler
from retainium.diagnostics import Diagnostics

def load_config():
    config = ConfigParser()
    config_path = os.path.join("etc", "config.ini")
    if not os.path.exists(config_path):
        Diagnostics.warn(f"Config file not found at {config_path}, using default settings")
    config.read(config_path)
    return config

def main():
    config = load_config()

    db_path = config.get("database", "path", fallback="data/knowledge_db")
    model_name = config.get("embeddings", "model", fallback="all-MiniLM-L6-v2")

    knowledge_db = KnowledgeDatabase(db_path)
    embedding_handler = EmbeddingHandler(model_name=model_name)
    llm_handler = LLMHandler(config) if config.getboolean("llm", "enabled", fallback=False) else None

    try:
        process_cli(knowledge_db, embedding_handler, llm_handler)
        Diagnostics.note("Operation completed.")
    except Exception as e:
        Diagnostics.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
