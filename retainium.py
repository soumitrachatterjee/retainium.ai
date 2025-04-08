# retainium.py

import os
from configparser import ConfigParser
from retainium.cli import process_cli
from retainium.knowledge import KnowledgeDB
from retainium.embeddings import EmbeddingHandler
from retainium.llm import LLMHandler
from retainium.diagnostics import Diagnostics

def load_config():
    config = ConfigParser()
    config.read(os.path.join("etc", "config.ini"))
    return config

def main():
    config = load_config()

    db_path = config.get("database", "path", fallback="data/knowledge_db")
    model_name = config.get("embeddings", "model", fallback="all-MiniLM-L6-v2")

    knowledge_db = KnowledgeDB(db_path)
    embedding_handler = EmbeddingHandler(model_name)  # Pass the model name string
    llm_handler = LLMHandler(config) if config.getboolean("llm", "enabled", fallback=False) else None

    process_cli(knowledge_db, embedding_handler, llm_handler)

if __name__ == "__main__":
    main()
