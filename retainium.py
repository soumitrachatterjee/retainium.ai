#
# retainium.ai
#    A local knowledge database and retrieval system that allows users to 
# store, semantically search, and query information using embeddings and a 
# locally hosted Large Language Model (LLM). 
# It is modular, privacy-respecting, and can run entirely offline.
#

# Import required modules
from retainium.diagnostics import Diagnostics
from retainium.config import load_config
from retainium.embeddings import EmbeddingHandler

# WIP
from retainium.cli import process_cli
from retainium.knowledge import KnowledgeDB

# TODO
from retainium.llm import LLMHandler

def main():
    config = load_config()

    model_name = config.get("embeddings", "model", fallback="all-MiniLM-L6-v2")
    Diagnostics.note(f"configured embeddings model name: {model_name}")
    embedding_handler = EmbeddingHandler(model_name=model_name)

    llm_handler = LLMHandler(config) if config.getboolean("llm", "enabled", fallback=False) else None
    Diagnostics.note(f"configured LLM: {llm_handler}")

    db_path = config.get("database", "path", fallback="data/knowledge_db")
    Diagnostics.note(f"configured database path: {db_path}")
    knowledge_db = KnowledgeDB(db_path)

    try:
        # Process command line options
        process_cli(knowledge_db, embedding_handler, llm_handler)

    except Exception as e:
        Diagnostics.error(f"failed to parse command line options: {e}")

if __name__ == "__main__":
    main()
